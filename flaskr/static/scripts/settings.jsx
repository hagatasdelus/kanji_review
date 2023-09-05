import React, { useState } from 'react';

const TypingGame = () => {
  const [soundEnabled, setSoundEnabled] = useState(true);

  const handleSoundToggle = () => {
    setSoundEnabled(!soundEnabled);
  };

  return (
    <>
      <label>
        <input type="checkbox" checked={soundEnabled} onChange={handleSoundToggle} />
        SEを有効にする
      </label>
    </>
  );
};
