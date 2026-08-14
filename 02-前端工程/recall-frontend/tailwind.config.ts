/** Recall 暗黑二次元风格 - Tailwind 配置（深紫黑 + 霓虹紫粉渐变） */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      /* ── 色彩 ── */
      colors: {
        primary: {
          DEFAULT: '#A78BFA',
          hover: '#8B5CF6',
          light: '#251F4A', // 暗紫浅底（替代原浅蓝）
        },
        brand: {
          pink: '#EC4899',
          cyan: '#22D3EE',
        },
        surface: {
          DEFAULT: '#191631',    // 卡片深紫
          secondary: '#0E0C1D',  // 页面背景深紫黑
          tertiary: '#211C3D',   // 更高层
        },
        border: '#2D284D',
        ink: {
          primary: '#F1EFFC',
          secondary: '#A8A4CC',
          tertiary: '#6F6A99',
        },
        success: '#34D399',
        warning: '#FBBF24',
        error: '#FB7185',
        question: '#60A5FA',
        analysis: '#34D399',
        // 错题本 8 色（霓虹）
        cat: {
          blue: '#60A5FA',
          green: '#34D399',
          orange: '#FBBF24',
          purple: '#C084FC',
          pink: '#F472B6',
          cyan: '#22D3EE',
          amber: '#FACC15',
          indigo: '#818CF8',
        },
      },
      /* ── 字体 ── */
      fontFamily: {
        sans: [
          'PingFang SC', '-apple-system', 'BlinkMacSystemFont', 'SF Pro Text',
          'SF Pro Display', 'Helvetica Neue', 'Arial', 'sans-serif',
        ],
        mono: ['SF Mono', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      /* ── 圆角 ── */
      borderRadius: {
        tag: '6px',
        btn: '8px',
        card: '14px',
        modal: '16px',
        panel: '20px',
        full: '24px',
      },
      /* ── 间距 (8px 栅格) ── */
      spacing: {
        xs: '4px',
        sm: '8px',
        md: '12px',
        lg: '16px',
        xl: '24px',
        '2xl': '32px',
        '3xl': '48px',
      },
      /* ── 毛玻璃 ── */
      backdropBlur: {
        glass: '40px',
      },
      /* ── 动效 ── */
      transitionDuration: {
        mac: '250ms',
      },
      transitionTimingFunction: {
        mac: 'cubic-bezier(0.25, 0.1, 0.25, 1)',
      },
      /* ── 霓虹发光 ── */
      boxShadow: {
        'mac-sm': '0 0 12px rgba(167,139,250,.12)',
        'mac': '0 0 20px rgba(167,139,250,.25)',
        'mac-lg': '0 8px 40px rgba(139,92,246,.35)',
        'mac-focus': '0 0 0 3px rgba(167,139,250,.35)',
        glow: '0 0 16px rgba(167,139,250,.35)',
        'glow-strong': '0 0 26px rgba(236,72,153,.45)',
      },
    },
  },
  plugins: [],
}
