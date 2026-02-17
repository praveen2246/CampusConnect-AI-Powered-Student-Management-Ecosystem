import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import TemplateEditor from './pages/TemplateEditor';

// Global Fonts
import "@fontsource/inter/400.css";
import "@fontsource/inter/500.css";
import "@fontsource/inter/600.css";
import "@fontsource/inter/700.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/700.css";

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/templates" element={<TemplateEditor />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
