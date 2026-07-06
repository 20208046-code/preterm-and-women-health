function BlankPage1() {
  return (
    <div className="page-wrapper">
      <div
        className="main-content"
        style={{
          maxWidth: '900px',
          margin: '0 auto',
          padding: '650px 20px 40px',
          textAlign: 'left',
        }}
      >
        <h2 className="section-title" style={{ color: 'white', fontSize: '2rem', marginBottom: '20px', textAlign: 'center' }}>
          Pregnancy Symptoms Checker
        </h2>

        <p className="intro-paragraph" style={{ marginBottom: '70px' }}>
          Early pregnancy symptoms vary from person to person. Some may feel symptoms within days of conception,
          while others may not notice until weeks later. Below is a guide to help you recognize common and uncommon
          signs of early pregnancy.
        </p>

        {/* Symptom Cards Section */}
        <div className="symptom-cards">
          <div className="symptom-card highlight-strong-text">
            <div className="card-circle">
              <img src="/pic2.png" alt="Icon" className="circle-img" />
            </div>
            <div className="card-content">
              <h3> Common Early Pregnancy Symptoms</h3>
              <ul>
                <li><strong>Missed Period:</strong> Often the first and most obvious sign.</li>
                <li><strong>Frequent Urination:</strong> Caused by increased blood volume and kidney activity.</li>
                <li><strong>Fatigue:</strong> Due to high levels of the hormone progesterone.</li>
                <li><strong>Morning Sickness:</strong> May begin as early as two weeks in.</li>
                <li><strong>Tender or Swollen Breasts:</strong> May feel sore or heavier than usual.</li>
              </ul>
            </div>
          </div>

          <div className="symptom-card blue-strong-text">
            <div className="card-circle">
              <img src="/blue.png" alt="Less Common Symptoms Icon" className="circle-img" />
            </div>
            <div className="card-content">
              <h3> Less Common Symptoms</h3>
              <ul>
                <li><strong>Spotting:</strong> Light bleeding 10 days after conception.</li>
                <li><strong>Food Cravings/Aversions:</strong> Changes in appetite or preferences.</li>
                <li><strong>Metallic Taste:</strong> Some describe tasting coins randomly.</li>
                <li><strong>Headaches/Dizziness:</strong> Caused by hormones and blood volume.</li>
                <li><strong>Bloating and Gas:</strong> Due to hormonal changes.</li>
                <li><strong>Mood Swings:</strong> Hormonal surges can affect emotions.</li>
                <li><strong>Stuffy Nose:</strong> Hormones may dry out or congest nasal passages.</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Info Cards Section */}
        <div className="info-card-section">
          <div className="info-bar-card">
            <h3>🧪 When Should You Take a Pregnancy Test?</h3>
            <p>
              It’s best to take a pregnancy test about one week after your missed period. Testing too soon may result in a false negative.
            </p>
          </div>

          <div className="info-bar-card">
            <h3>📞 When to Contact a Healthcare Provider</h3>
            <p>
              If you’ve missed your period and tested positive, contact your provider. A preconception appointment is helpful if you’re planning pregnancy.
            </p>
          </div>
        </div>

        {/* Reference Link */}
        <p style={{ fontWeight: 'bold', marginTop: '60px', color: 'white' }}>
          🔗 For more detailed information on pregnancy symptoms, visit: <br />
          <a
            href="https://my.clevelandclinic.org/health/articles/9709-pregnancy-am-i-pregnant"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#fa9dc0', fontWeight: 'bold', textDecoration: 'underline' }}
          >
            Cleveland Clinic – Pregnancy Symptoms Overview
          </a>
        </p>

        {/* Disclaimer */}
        <p className="disclaimer-note">
          Please note: These symptoms are for informational purposes only. Always consult with a healthcare provider for a proper diagnosis.
        </p>
      </div>
      <footer className="site-footer">
        <p>&copy; {new Date().getFullYear()} Preterm and Women Health. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default BlankPage1;
