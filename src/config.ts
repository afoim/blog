import type {
  LicenseConfig,
  NavBarConfig,
  ProfileConfig,
  SiteConfig,
} from './types/config'
import { LinkPreset } from './types/config'

export const siteConfig: SiteConfig = {
  title: '二叉树树的博客',
  subtitle: '爱你所爱！',
  lang: 'zh_CN',         // 'en', 'zh_CN', 'zh_TW', 'ja', 'ko'
  themeColor: {
    hue: 355,         // Default hue for the theme color, from 0 to 360. e.g. red: 0, teal: 200, cyan: 250, pink: 345
    fixed: false,     // Hide the theme color picker for visitors
  },
  banner: {
    enable: true,
    src: 'assets/images/222.jpg',   // Relative to the /src directory. Relative to the /public directory if it starts with '/'
    position: 'center',      // Equivalent to object-position, only supports 'top', 'center', 'bottom'. 'center' by default
    credit: {
      enable: false,         // Display the credit text of the banner image
      text: '',              // Credit text to be displayed
      url: ''                // (Optional) URL link to the original artwork or artist's page
    }
  },
  favicon: [    // Leave this array empty to use the default favicon
     {
       src: 'https://q2.qlogo.cn/headimg_dl?dst_uin=2973517380&spec=5',    // Path of the favicon, relative to the /public directory
       //theme: 'light',              // (Optional) Either 'light' or 'dark', set only if you have different favicons for light and dark mode
       sizes: '128x128',              // (Optional) Size of the favicon, set only if you have favicons of different sizes
     }
  ]
}

export const navBarConfig: NavBarConfig = {
  links: [
    LinkPreset.Home,
    LinkPreset.Archive,
    LinkPreset.About,
    {
      name: '随机图',
      url: 'https://pic.onani.cn',     // Internal links should not include the base path, as it is automatically added
      external: true,                               // Show an external link icon and will open in a new tab
    },
    {
      name: 'GitHub',
      url: 'https://github.com/saicaca/fuwari',     // Internal links should not include the base path, as it is automatically added
      external: true,                               // Show an external link icon and will open in a new tab
    },
  ],
}

export const profileConfig: ProfileConfig = {
  avatar: 'https://q2.qlogo.cn/headimg_dl?dst_uin=2973517380&spec=5',  // Relative to the /src directory. Relative to the /public directory if it starts with '/'
  name: '二叉树树',
  bio: 'Protect What You Love./爱你所爱！',
  links: [
    // {
      // name: 'Twitter',
      // icon: 'fa6-brands:twitter',       // Visit https://icones.js.org/ for icon codes
                                        // You will need to install the corresponding icon set if it's not already included
                                        // `pnpm add @iconify-json/<icon-set-name>`
      // url: 'https://twitter.com',
    // },
    // {
      // name: 'Steam',
      // icon: 'fa6-brands:steam',
      // url: 'https://store.steampowered.com',
    // },
    {
      name: 'GitHub',
      icon: 'fa6-brands:github',
      url: 'https://github.com/afoim',
    },
    {
      name: 'QQ',
      icon: 'fa6-brands:qq',
      url: 'https://qm.qq.com/q/Uy9kmDXHYO',
    },
    {
      name: 'QQ',
      icon: 'fa6-solid:envelope',
      url: 'mailto:acofork@foxmail.com',
    },
  ],
}

export const licenseConfig: LicenseConfig = {
  enable: true,
  name: 'CC BY-NC-SA 4.0',
  url: 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
}
