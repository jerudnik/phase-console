import { LogoProps } from './types'

export const KanidmLogo = ({ className }: LogoProps) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    className={className}
  >
    <rect x="2" y="2" width="20" height="20" rx="5" className="fill-[#5d2de0]" />
    <path
      d="M8 6.5h2.4v4.2l3.5-4.2H16.8l-3.9 4.6 4.1 6.4h-2.8l-2.9-4.6-1.4 1.6v3H8z"
      className="fill-white"
    />
  </svg>
)
