function BlankPage2() {
  return (
    <div className="page-wrapper">
      <div className="main-content" style={{ maxWidth: '1200px', margin: '0 auto', paddingTop: '350px' }}>
        <h2 className="section-title" style={{ textAlign: 'center', color: 'white', fontSize: '2.4rem', marginBottom: '20px' }}>
          Pregnancy Complications
        </h2>

        <p className="intro-paragraph" style={{ textAlign: 'left', marginBottom: '60px', color: 'white', fontSize: '1.1rem' }}>
          Although most pregnancies progress without major issues, some expectant mothers may encounter complications that require careful monitoring. Conditions like high blood pressure or gestational diabetes can affect both maternal and fetal health, while problems with amniotic fluid levels or placental positioning may lead to discomfort or preterm labor. Early detection through regular check-ups and open communication with healthcare providers can help manage risks and promote a safer, healthier journey to childbirth.
        </p>

        <div className="symptom-cards" style={{ display: 'flex', flexWrap: 'nowrap', justifyContent: 'space-between', gap: '20px', flexDirection: 'row' }}>
          <div className="symptom-card highlight-strong-text" style={{ flex: '1', display: 'flex', flexDirection: 'column', justifyContent: 'flex-start' }}>
            <div style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '10px' }}>💧</div>
            <div className="card-content">
              <h3>Amniotic Fluid Complications</h3>
              <ul>
                <li><strong>Too much fluid:</strong> May cause preterm labor, early rupture of membranes, maternal breathing issues.</li>
                <li><strong>Too little fluid:</strong> Linked to birth defects, placental problems, fetal growth restriction or fetal death.</li>
                <li><strong>Causes:</strong> Diabetes, infections, multiple pregnancy, birth defects, blood incompatibility.</li>
              </ul>
            </div>
          </div>

          <div className="symptom-card blue-strong-text" style={{ flex: '1', display: 'flex', flexDirection: 'column', justifyContent: 'flex-start' }}>
            <div style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '10px' }}>❗</div>
            <div className="card-content">
              <h3>Bleeding During Pregnancy</h3>
              <ul>
                <li>Early or late bleeding could signal <strong>placental issues, infections, or preterm labor</strong>.</li>
                <li><strong>Always report</strong> bleeding immediately to a healthcare provider.</li>
              </ul>
            </div>
          </div>

          <div className="symptom-card highlight-strong-text" style={{ flex: '1', display: 'flex', flexDirection: 'column', justifyContent: 'flex-start' }}>
            <div style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '10px' }}>⚠️</div>
            <div className="card-content">
              <h3>Ectopic Pregnancy</h3>
              <ul>
                <li>Occurs when the embryo implants outside the uterus (often in fallopian tubes).</li>
                <li>Can be <strong>life-threatening</strong> and requires urgent care.</li>
                <li><strong>Symptoms:</strong> Abdominal pain, bleeding, occurs ~3–6 weeks after missed period.</li>
                <li><strong>Treatment:</strong> Medication or surgery.</li>
              </ul>
            </div>
          </div>

          <div className="symptom-card blue-strong-text" style={{ flex: '1', display: 'flex', flexDirection: 'column', justifyContent: 'flex-start' }}>
            <div style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '10px' }}>🧷</div>
            <div className="card-content">
              <h3>Placental Complications</h3>
              <ul>
                <li><strong>Placental Abruption:</strong> Premature separation from the uterine wall.</li>
                <li><strong>Symptoms:</strong> Vaginal bleeding, pain, tenderness. May require early delivery.</li>
                <li><strong>Placenta Previa:</strong> Placenta covers or is near cervix.</li>
                <li><strong>Symptoms:</strong> Bright red bleeding, abdominal discomfort. Often requires C-section.</li>
              </ul>
            </div>
          </div>
        </div>

        <p style={{ marginTop: '50px', textAlign: 'center', fontWeight: 'bold', color: 'white', fontSize: '1.05rem' }}>
          🔗 For more information about pregnancy complications, please visit:
          <br />
          <a
            href="https://www.hopkinsmedicine.org/health/conditions-and-diseases/staying-healthy-during-pregnancy/complications-of-pregnancy"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#fa9dc0', textDecoration: 'underline' }}
          >
            Johns Hopkins Medicine – Pregnancy Complications
          </a>
        </p>
      </div>
      <footer className="site-footer">
        <p>&copy; {new Date().getFullYear()} Preterm and Women Health. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default BlankPage2;
