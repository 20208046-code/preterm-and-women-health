import { Link, Outlet } from 'react-router-dom';
import './App.css';

function Layout() {
  return (
    <>
      <nav className="navbar">
        <div className="navbar-left">
          <img src="/1logo.png"alt="Logo" className="logo" />
          <span className="navbar-title">Preterm and Women Health</span>
        </div>
        <div className="navbar-right">
          <Link to="/" className="nav-link">Home</Link>
        </div>
      </nav>

      <Outlet />
    </>
  );
}

export default Layout;
