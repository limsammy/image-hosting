import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ErrorBoundary from './components/ErrorBoundary';
import ProtectedRoute from './components/ProtectedRoute';
import DesignSystem from './pages/DesignSystem';
import Login from './pages/Login';
import Gallery from './pages/Gallery';

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            {/* Design System Route (public for development) */}
            <Route path="/design-system" element={<DesignSystem />} />

            {/* Public Auth Pages */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<ComingSoon page="Register" />} />

            {/* Protected App Pages */}
            <Route
              path="/gallery"
              element={
                <ProtectedRoute>
                  <Gallery />
                </ProtectedRoute>
              }
            />

            {/* Redirect root to gallery (protected) */}
            <Route path="/" element={<Navigate to="/gallery" replace />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </ErrorBoundary>
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
