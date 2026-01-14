import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import DesignSystem from './pages/DesignSystem';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Design System Route */}
        <Route path="/design-system" element={<DesignSystem />} />

        {/* Placeholder routes for future pages */}
        <Route path="/login" element={<ComingSoon page="Login" />} />
        <Route path="/register" element={<ComingSoon page="Register" />} />
        <Route path="/gallery" element={<ComingSoon page="Gallery" />} />

        {/* Redirect root to design system for now */}
        <Route path="/" element={<Navigate to="/design-system" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

function ComingSoon({ page }: { page: string }) {
  return (
    <div className="min-h-screen bg-bg-primary flex items-center justify-center">
      <div className="text-center">
        <h1 className="heading-2 mb-4">{page}</h1>
        <p className="body-base text-text-secondary mb-8">This page is coming soon.</p>
        <a href="/design-system" className="btn-primary">
          View Design System
        </a>
      </div>
    </div>
  );
}

export default App;
