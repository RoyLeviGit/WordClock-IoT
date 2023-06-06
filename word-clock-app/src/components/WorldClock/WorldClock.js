import React, { useState, useEffect } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

import "./WorldClock.css";

const WorldClock = () => {
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('United States');

  useEffect(() => {
    const fetchCountries = async () => {
      const response = await fetch('https://restcountries.com/v2/all');
      const data = await response.json();
      setCountries(data.map((country) => country.name));
    };

    fetchCountries();
  }, []);

 
  const handleCountryChange = async () => {
    const response = await fetch('/change-country', {
      method: 'POST',
      body: JSON.stringify({ country: selectedCountry }),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    console.log(data);
  };

  return (
    <div className='world-clock'>
        <Autocomplete style={{width: 300, margin:10}}
        value={selectedCountry}
        onChange={(event, newValue) => {
          setSelectedCountry(newValue);
        }}
        options={countries}
        renderInput={(params) => (
          <TextField {...params} label="Choose a country" variant="outlined" />
        )}
        />
        <Button style={{margin:10}} variant="contained" onClick={handleCountryChange} sx={{ backgroundColor: '#47585F' }}>Change Time Zone</Button>
    </div>
  );
};

export default WorldClock;
