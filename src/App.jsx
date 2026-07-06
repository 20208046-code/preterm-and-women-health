import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './Layout';
import BlankPage1 from './pages/BlankPage1';
import BlankPage2 from './pages/BlankPage2';
import BlankPage3 from './pages/BlankPage3';
import BlankPage4 from './pages/BlankPage4';
import BlankPage5 from './pages/BlankPage5';

function HomePage() {
  return (
    <div className="page-wrapper">
      <div className="hero-section">
        <h1 className="site-title">Preterm and Women Health</h1>
        <p className="quote">“With every newborn baby, a little sun rises.”</p>
      </div>

      <div className="main-content">
        <div className="intro-paragraph">
          <p>
            Prenatal care plays an incredibly important role in supporting maternal and fetal health.
            It encompasses a range of medical, nutritional, and emotional support services that are
            aimed at helping women have a healthy, happy, and successful pregnancy.
          </p>
          <p>
            For each woman, prenatal care will look slightly different. That’s because all aspects
            of prenatal care should be tailored to each pregnancy and encompass best practices around
            checkups, screenings, nutrition, exercise and overall wellness.
          </p>
          <p>
            Here are some general tips to help you get started on your journey towards a healthy pregnancy.
          </p>
        </div>

        <div className="card-section">
          <a href="/symptoms" className="info-card">
            <img src="9851973_4291557-removebg-preview.png" alt="Discharge" className="card-icon" />
            <h3>Pregnancy Symptoms Checker</h3>
            <p>"Quickly assess common symptoms and understand what’s normal or when to seek medical advice."</p>
          </a>

          <a href="/complications" className="info-card">
            <img src="2722602.png" alt="Headache" className="card-icon" />
            <h3>Pregnancy Complications</h3>
            <p>"Be aware of symptoms that may indicate risks to you or your baby during pregnancy."</p>
          </a>

          <a href="/ovulation" className="info-card">
            <img src="ovulation_calculator.png" alt="Fever" className="card-icon" />
            <h3>Ovulation Calculator</h3>
            <p>"Estimate your most fertile days to boost your chances of conception."</p>
          </a>

          <a href="/preterm" className="info-card">
            <img src="3d-illustration-icon-of-pink-email-with-checklist-for-ui-ux-web-mobile-app-social-media-ads-png.png" alt="Checklist" className="card-icon" />
            <h3>Preterm Accuracy Detection</h3>
            <p>"Leverages predictive tools to assess the risk of premature birth with greater precision."</p>
          </a>

          <a href="/ultrasound" className="info-card">
            <img src="download.png" alt="Ultrasound" className="card-icon" />
            <h3>Fetal Head Ultrasounds</h3>
            <p>"Monitor brain development and detect potential concerns early through detailed imaging."</p>
          </a>
        </div>
      </div>

      <footer className="site-footer">
        <p>&copy; {new Date().getFullYear()} Preterm and Women Health. All rights reserved.</p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="symptoms" element={<BlankPage1 />} />
          <Route path="complications" element={<BlankPage2 />} />
          <Route path="ovulation" element={<BlankPage3 />} />
          <Route path="preterm" element={<BlankPage4 />} />
          <Route path="ultrasound" element={<BlankPage5 />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
