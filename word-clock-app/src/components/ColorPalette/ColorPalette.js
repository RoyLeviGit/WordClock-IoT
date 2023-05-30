import React, { useState } from 'react';
import reactCSS from 'reactcss';
import { ChromePicker } from 'react-color';
import { Button, IconButton } from '@mui/material';


const ColorPalette = () => {
  const [displayColorPicker, setDisplayColorPicker] = useState(false);
  const [color, setColor] = useState('#e74c3c');

  const handleClick = () => {
    setDisplayColorPicker(!displayColorPicker);
  };

  const handleClose = () => {
    setDisplayColorPicker(false);
  };

  const handleChange = (selectedColor) => {
    setColor(selectedColor.hex);
  };

  const handleSendColor = () => {
    // Perform your fetch request to send the color to the backend here
    // Example code:
    console.log(color);
    fetch('/api/send-color', {
      method: 'POST',
      body: JSON.stringify({ color }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response from the backend
      })
      .catch((error) => {
        // Handle any errors that occurred during the fetch request
      });
  };

  const styles = reactCSS({
    'default': {
      color: {
        width: '36px',
        height: '36px',
        borderRadius: '50%',
        background: color,
      },
      swatch: {
        padding: '5px',
        background: '#fff',
        borderRadius: '50%',
        boxShadow: '0 0 0 1px rgba(0,0,0,.1)',
        display: 'inline-block',
        cursor: 'pointer',
      },
      popover: {
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        zIndex: '1',
      },
      buttonContainer: {
        display: 'flex',
        justifyContent: 'center',
        marginTop: '10px',
      },
      button: {
        marginRight: '10px',
      },
    },
  });

  return (
    <div style={{display: 'flex', alignItems: 'center', flexDirection: 'column'}}>
      <h5>Please pick a color for the clock</h5>
      <div style={styles.swatch} onClick={handleClick}>
        <div style={styles.color} />
      </div>
      {displayColorPicker && (
        <div style={{marginTop: 10}}>
          <ChromePicker color={color} onChange={handleChange} disableAlpha />
          <div style={styles.buttonContainer}>
            {/* <Button variant="contained" sx={{ marginTop: 2, backgroundColor: '#47585F'}} onClick={handleClose}>
              Cancel
            </Button> */}
          </div>
        </div>
      )}
      <Button variant="contained" sx={{ marginTop: 2, marginBottom: 3, backgroundColor: '#47585F'}} onClick={handleSendColor}>
        Set Color
      </Button>
    </div>
  );
};

export default ColorPalette;
