import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '@epam/uui-components/styles.css'
import '@epam/uui/styles.css'
import '@epam/assets/theme/theme_eduverse_light.scss'
import '@epam/assets/theme/theme_eduverse_dark.scss'
import './index.module.scss'
import App from './App.tsx'
import { ThemeProvider } from './components/ThemeProvider/ThemeProvider'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>,
)
