import os
import sys
import shutil
import re
from datetime import datetime
from pathlib import Path
from PIL import Image
import yaml
from tqdm import tqdm
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed

PROGRESS_BAR_FORMAT = {
    'ncols': 80,
    'bar_format': '{desc}: {percentage:3.0f}% |{bar:25}| {n_fmt}/{total_fmt}',
    'ascii': '⣀⣄⣤⣦⣶⣷⣿'
}

class MarkdownImageProcessor:
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)
        self.parent_dir = self.source_dir.parent
        self.image_references = set()
        self.unreferenced_images = []
        self.error_logs = []
        self.cpu_count = multiprocessing.cpu_count()

    def create_backup(self):
        """创建源目录的备份"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_name = f"{self.source_dir.name}backup{timestamp}"
        backup_path = self.parent_dir / backup_name
        
        try:
            total_files = sum(1 for _ in self.source_dir.rglob('*'))
            with tqdm(total=total_files, desc="创建备份", **PROGRESS_BAR_FORMAT) as pbar:
                def copy_with_progress(src, dst, *args, **kwargs):
                    shutil.copy2(src, dst, *args, **kwargs)
                    pbar.update(1)
                
                shutil.copytree(self.source_dir, backup_path, copy_function=copy_with_progress)
            print(f"备份已创建: {backup_path}")
            return True
        except Exception as e:
            print(f"备份创建失败: {e}")
            return False

    def extract_image_paths(self, content):
        """从Markdown内容中提取所有图片路径"""
        # 从frontmatter中提取图片路径
        image_path = self.extract_image_paths_from_frontmatter(content)
        if image_path:
            yield image_path.replace('\\', '/')
        
        # 从正文中提取图片路径
        paths = re.findall(r'!\[.*?\]\((.*?)\)', content)
        for path in paths:
            yield path.strip().lstrip('./').replace('\\', '/')

    def extract_image_paths_from_frontmatter(self, content):
        """从Markdown文件的frontmatter中提取图片路径"""
        try:
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if match:
                frontmatter = yaml.safe_load(match.group(1))
                if isinstance(frontmatter, dict):
                    image_path = frontmatter.get('image', '')
                    if image_path:
                        return image_path.strip("'\"").lstrip('./')
        except Exception as e:
            self.error_logs.append(f"解析frontmatter失败: {e}")
        return None

    def scan_markdown_files(self):
        """扫描所有Markdown文件并收集图片引用"""
        md_files = list(self.source_dir.glob('*.md'))
        md_count = len(md_files)

        def process_file(md_file):
            try:
                content = md_file.read_text(encoding='utf-8')
                for image_path in self.extract_image_paths(content):
                    self.image_references.add(image_path)
            except Exception as e:
                self.error_logs.append(f"处理Markdown文件 {md_file} 失败: {e}")

        with ThreadPoolExecutor(max_workers=self.cpu_count) as executor:
            list(tqdm(executor.map(process_file, md_files), total=md_count, desc="扫描Markdown文件", **PROGRESS_BAR_FORMAT))

        print(f"共扫描到 {md_count} 个Markdown文档")
        return md_count

    def find_unreferenced_images(self):
        """查找未被引用的图片文件"""
        image_extensions = {'.png', '.jpg', '.jpeg', '.webp'}
        all_images = []

        for img_dir in set(str(Path(p).parent).replace('\\', '/') for p in self.image_references):
            dir_path = self.source_dir / img_dir
            if dir_path.exists():
                all_images.extend(dir_path.glob('*'))

        def check_image(img_file):
            relative_path = str(img_file.relative_to(self.source_dir)).replace('\\', '/')
            if relative_path not in self.image_references:
                return relative_path
            return None

        with ThreadPoolExecutor(max_workers=self.cpu_count) as executor:
            results = list(tqdm(executor.map(check_image, all_images), total=len(all_images), desc="检查未引用图片", **PROGRESS_BAR_FORMAT))

        self.unreferenced_images = [res for res in results if res]
        print(f"未被引用的图片路径: {self.unreferenced_images}")

    def convert_to_webp(self):
        """将所有引用的非webp图片转换为webp格式"""
        converted_files = []

        def convert_image(img_path):
            full_path = self.source_dir / img_path
            if full_path.suffix.lower() == '.webp':
                return None  # 跳过WebP文件
            if not full_path.exists():
                self.error_logs.append(f"图片文件不存在: {img_path}")
                return None

            try:
                new_path = full_path.with_suffix('.webp')
                with Image.open(full_path) as img:
                    img.save(str(new_path), 'WEBP', quality=80)
                full_path.unlink()  # 删除原文件
                return img_path
            except Exception as e:
                self.error_logs.append(f"转换图片失败 {img_path}: {e}")
                return None

        with ThreadPoolExecutor(max_workers=self.cpu_count) as executor:
            results = list(tqdm(executor.map(convert_image, self.image_references), total=len(self.image_references), desc="转换图片到WebP", **PROGRESS_BAR_FORMAT))

        converted_files = [res for res in results if res]
        return converted_files

    def update_markdown_files(self, converted_files):
        """更新所有Markdown文件中的图片引用"""
        md_files = list(self.source_dir.glob('*.md'))
        
        with tqdm(md_files, desc="更新Markdown文件", **PROGRESS_BAR_FORMAT) as pbar:
            for md_file in pbar:
                try:
                    content = md_file.read_text(encoding='utf-8')
                    modified = False

                    for old_path in converted_files:
                        new_path = str(Path(old_path).with_suffix('.webp')).replace('\\', '/')
                        content = content.replace(old_path.replace('\\', '/'), new_path)
                        
                        pattern = f'\\]\\({re.escape(old_path.replace("\\", "/"))}\\)'
                        if re.search(pattern, content):
                            content = re.sub(pattern, f']({new_path})', content)
                            modified = True

                    if modified:
                        md_file.write_text(content, encoding='utf-8')

                except Exception as e:
                    self.error_logs.append(f"更新Markdown文件失败 {md_file}: {e}")
                
                pbar.set_postfix({"当前文件": md_file.name})

    def delete_unreferenced_images(self):
        """删除未被引用的图片"""
        with tqdm(self.unreferenced_images, desc="删除未引用图片", **PROGRESS_BAR_FORMAT) as pbar:
            for img_path in pbar:
                try:
                    full_path = self.source_dir / img_path
                    if full_path.exists():
                        full_path.unlink()
                except Exception as e:
                    self.error_logs.append(f"删除未引用图片失败 {img_path}: {e}")
                pbar.set_postfix({"当前文件": img_path})

def main():
    if len(sys.argv) != 2:
        print("用法: python app.py <目录路径>")
        return

    source_dir = sys.argv[1]
    if not os.path.isdir(source_dir):
        print(f"错误: {source_dir} 不是有效的目录")
        return

    processor = MarkdownImageProcessor(source_dir)

def main():
    if len(sys.argv) != 2:
        print("用法: python app.py <目录路径>")
        return

    source_dir = sys.argv[1]
    if not os.path.isdir(source_dir):
        print(f"错误: {source_dir} 不是有效的目录")
        return

    processor = MarkdownImageProcessor(source_dir)

    # 阶段零 - 全备份
    print("阶段零 - 创建备份...")
    if not processor.create_backup():
        print("备份失败,程序终止")
        return

    # 阶段一 - 扫描无用资源
    print("\n阶段一 - 扫描资源...")
    md_count = processor.scan_markdown_files()
    processor.find_unreferenced_images()

    print(f"\n扫描结果:")
    print(f"- 共扫描到 {md_count} 个MarkDown文档")
    print(f"- 引用资源数: {len(processor.image_references)} 个")
    print(f"- 未被任何引用的资源数: {len(processor.unreferenced_images)} 个")

    if processor.error_logs:
        print("\n扫描过程中发现以下问题:")
        for error in processor.error_logs:
            print(f"- {error}")

    if processor.unreferenced_images:
        print("\n未被引用的资源:")
        for img in processor.unreferenced_images:
            print(f"- {img}")

    # 自动删除未引用资源
    print("\n删除未引用资源并继续处理...")
    processor.delete_unreferenced_images()
    print("已删除未引用资源")

    # 阶段二 - 转换资源
    print("\n阶段二 - 转换资源为WebP格式...")
    converted_files = processor.convert_to_webp()
    
    if converted_files:
        print("更新Markdown文件中的资源引用...")
        processor.update_markdown_files(converted_files)

    if processor.error_logs:
        print("\n处理过程中发现以下问题:")
        for error in processor.error_logs:
            print(f"- {error}")

    # 自动修改图片扩展名为 .webp
    print("\n阶段三 - 修改图片扩展名为 .webp ...")
    md_files = list(processor.source_dir.glob('*.md'))
    with tqdm(md_files, desc="更新文件扩展名", **PROGRESS_BAR_FORMAT) as pbar:
        for md_file in pbar:
            try:
                content = md_file.read_text(encoding='utf-8')
                # 替换多种图片格式扩展名
                for ext in ['.png', '.jpg', '.jpeg']:
                    content = content.replace(ext, '.webp')

                if content != md_file.read_text(encoding='utf-8'):
                    md_file.write_text(content, encoding='utf-8')
            except Exception as e:
                processor.error_logs.append(f"更新Markdown文件 {md_file} 扩展名失败: {e}")
            pbar.set_postfix({"当前文件": md_file.name})

    print("\n扩展名修改完成。")

    print("\n处理完成!")

if __name__ == "__main__":
    main()
