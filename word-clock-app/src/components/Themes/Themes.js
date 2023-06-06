import React, { useState } from 'react';
import { Button, FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import "./Themes.css";

const Themes = () => {
  const [selectedTheme, setSelectedTheme] = useState('');

  const handleChange = (event) => {
    setSelectedTheme(event.target.value);
  };

  const handleSetTheme = () => {
    // Send fetch request to the backend with the selected theme
    fetch('/set-theme', {
      method: 'POST',
      body: JSON.stringify({ theme: selectedTheme }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        // Handle the response data
        console.log(data);
      })
      .catch(error => {
        // Handle any errors
        console.error(error);
      });
  };

  return (
    <div className='div-themes'>
        <div className='div-themes-selector'>
            <FormControl style={{width: 300, margin:10}}>
                <InputLabel id="theme-label">Select Theme</InputLabel>
                <Select
                labelId="theme-label"
                id="theme-select"
                value={selectedTheme}
                label="Select Theme"
                onChange={handleChange}
                >
                <MenuItem value="theme1">Holiday</MenuItem>
                <MenuItem value="theme2">Birthday</MenuItem>
                <MenuItem value="theme3">Random</MenuItem>
                {/* Add more menu items for different themes */}
                </Select>
            </FormControl>
        </div>
        <div className='div-themes-button'>
            <Button variant="contained" onClick={handleSetTheme} sx={{marginBottom: 3, backgroundColor: '#47585F'}}>Set Theme</Button>
        </div>
    </div>
  );
};

export default Themes;
