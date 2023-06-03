import React, { useState } from "react";
import { TextField, Button } from "@mui/material";
import "./AlarmClock.css"

function DateTimePicker() {
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedHour, setSelectedHour] = useState("");

  const handleDateChange = (event) => {
    setSelectedDate(event.target.value);
  };

  const handleHourChange = (event) => {
    setSelectedHour(event.target.value);
  };

  const handleSearch = () => {
    const hourToSend = selectedHour;
  
    // Send the selected hour to the backend
    fetch('/set_hour', {
      method: 'POST',
      body: JSON.stringify({ hour: hourToSend }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to send hour to backend');
      }
      return response.json();
    })
    .then(data => {
      // Do something with the response data, if needed
      console.log(data);
    })
    .catch(error => {
      console.error(error);
    });
  };
  

  return (
    <div className="alarm-clock">
        <h2>Alarm Clock</h2>
        <div className="alarm-clock-date-selection">
            <TextField style={{margin: 10}}
            id="date"
            // label="Select Date"
            type="date"
            value={selectedDate}
            onChange={handleDateChange}
            />
            <TextField style={{margin: 10}}
            id="time"
            // label="Select Hour"
            type="time"
            value={selectedHour}
            onChange={handleHourChange}
            />
        </div>
        <Button variant="contained" color="primary" onClick={handleSearch}>
        Set Alarm
        </Button>
    </div>
  );
}

export default DateTimePicker;
