import React, { useState } from 'react';

const SettingForm = () => {
  const [circle, setCircle] = useState(false);
  const [nextQTime, setNextQTime] = useState(5);
  const [successSound, setSuccessSound] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = {
        circle,
        nextQTime,
        successSound
      };
      const response = await fetch('/api/submit-form', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      const result = await response.json();

  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        サークル表示:
        <input
          name="circle"
          type="checkbox"
          checked={circle}
          onChange={e => setCircle(e.target.checked)}
        />
      </label>
      <br />
      <label>
        次の問題までの秒数(5~20s):
        <input
          name="nextQTime"
          type="number"
          min="5"
          max="20"
          value={nextQTime}
          onChange={e => setNextQTime(e.target.value)}
        />
      </label>
      <br />
      <label>
        SE:
        <input
          name="successSound"
          type="checkbox"
          checked={successSound}
          onChange={e => setSuccessSound(e.target.checked)}
        />
      </label>
      <br />
      <input type="submit" value="設定" />
    </form>
  );
}

export default SettingForm;
