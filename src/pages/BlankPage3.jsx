import React, { useEffect, useState, useCallback } from 'react';

function BlankPage3() {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [lastPeriod, setLastPeriod] = useState('');
  const [cycleLength, setCycleLength] = useState(28);
  const [calendarDays, setCalendarDays] = useState([]);
  const nextPeriodDate = lastPeriod
    ? new Date(
        new Date(lastPeriod).setDate(
          new Date(lastPeriod).getDate() + parseInt(cycleLength)
        )
      )
    : null;

  const renderCalendar = useCallback(
    (baseDate) => {
      const days = [];
      const year = baseDate.getFullYear();
      const month = baseDate.getMonth();
      const start = new Date(year, month, 1);
      const end = new Date(year, month + 1, 0);

      const startDay = start.getDay();
      for (let i = 0; i < startDay; i++) {
        days.push(<div key={`empty-${i}`}></div>);
      }

      const lastPeriodDate = new Date(lastPeriod);
      const ovulationDay = cycleLength - 14;

      for (let i = 1; i <= end.getDate(); i++) {
        const date = new Date(year, month, i);
        const daysSince = (date - lastPeriodDate) / (1000 * 60 * 60 * 24);
        let className = 'day';

        if (!isNaN(lastPeriodDate)) {
          if (daysSince >= ovulationDay - 2 && daysSince <= ovulationDay + 2) {
            className += ' fertile';
          }
          if (Math.round(daysSince) === ovulationDay) {
            className = 'day ovulation';
          }
        }

        days.push(
          <div key={i} className={className}>
            {i}
          </div>
        );
      }

      setCalendarDays(days);
    },
    [lastPeriod, cycleLength]
  );

  useEffect(() => {
    renderCalendar(currentDate);
  }, [currentDate, renderCalendar]);

  const prevMonth = () =>
    setCurrentDate(
      new Date(currentDate.setMonth(currentDate.getMonth() - 1))
    );
  const nextMonth = () =>
    setCurrentDate(
      new Date(currentDate.setMonth(currentDate.getMonth() + 1))
    );

  return (
    <div className="page-wrapper">
      <div
        className="calendar-wrapper"
        style={{ paddingTop: '40px' /* push below navbar */ }}
      >
        <h2 style={{ marginBottom: '20px' }}>Ovulation Calculator</h2>

        <div className="date-picker" style={{ marginBottom: '20px' }}>
          <label htmlFor="lastPeriod">
            Select the first day of your last period:
          </label>
          <input
            type="date"
            id="lastPeriod"
            value={lastPeriod}
            onChange={(e) => setLastPeriod(e.target.value)}
          />
        </div>

        <div className="cycle-input" style={{ marginBottom: '20px' }}>
          <label htmlFor="cycleLength">How long is your average cycle?</label>
          <input
            type="number"
            id="cycleLength"
            value={cycleLength}
            onChange={(e) => setCycleLength(e.target.value)}
            min="20"
            max="45"
          />{' '}
          days
        </div>

        <div className="calendar-header">
          <button onClick={prevMonth}>&lt;</button>
          <div>
            {currentDate.toLocaleString('default', {
              month: 'long',
              year: 'numeric',
            })}
          </div>
          <button onClick={nextMonth}>&gt;</button>
        </div>

        <div className="calendar-grid">{calendarDays}</div>

        {nextPeriodDate && (
          <p className="note">
            📅 Your next estimated period is:{' '}
            <strong>{nextPeriodDate.toDateString()}</strong>
          </p>
        )}

        <p className="note">
          Note: Sperm can last up to 7 days and the egg for 24 hours. Having regular
          sex before, during and after these dates increases your chance of
          pregnancy.
        </p>
        <p className="note">
          This tool provides estimates only and should not be used as a medical
          reference.
        </p>
      </div>

      <footer className="site-footer">
        <p>
          &copy; {new Date().getFullYear()} Preterm and Women Health. All rights
          reserved.
        </p>
      </footer>
    </div>
  );
}

export default BlankPage3;
