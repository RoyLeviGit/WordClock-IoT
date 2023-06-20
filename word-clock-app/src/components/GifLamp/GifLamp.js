import React, { useState } from 'react';
import { Tabs, Tab, Box, TextField, Button, Typography } from '@mui/material';
import "./GifLamp.css";

const GifChooser = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const [gifUrl, setGifUrl] = useState('');

  const handleTabChange = (event, newValue) => {
    setTabIndex(newValue);
  };

  const handleGifUrlChange = (event) => {
    setGifUrl(event.target.value);
  };

  const handleGifDrop = (event) => {
    event.preventDefault();
    const gifFile = event.dataTransfer.files[0];
    const gifUrl = URL.createObjectURL(gifFile);
    setGifUrl(gifUrl);
  };

  const handleSendGifUrl = () => {
    console.log('Sending GIF URL:', gifUrl);

    if (gifUrl.startsWith('blob')) {
      fetch(gifUrl)
      .then(res => res.blob())  // convert the data to a blob
      .then(blob => {
        const formData = new FormData();
    
        // 'gif' is the name of the field to be used in the server side script
        formData.append('gif', blob, 'filename.gif');
    
        fetch('/gif', {
          method: 'POST',
          body: formData,
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
      });
    } else {
        // Send the URL to the server
        fetch('/gif_url', {
          method: 'POST',
          body: JSON.stringify({ gifUrl: gifUrl }),
          headers: {
            'Content-Type': 'application/json',
          },
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));      
    }
  };

  return (
    <div className='div-gif-lamp'>
        <h2>Gif Lamp</h2>
      <div>
        <Tabs value={tabIndex} onChange={handleTabChange} sx>
          <Tab label="Choose" style={{color: '#47585F'}}/>
          <Tab label="Paste URL" style={{color: '#47585F'}}/>
          <Tab label="Drag & Drop" style={{color: '#47585F'}}/>

        </Tabs>
      </div>
      {tabIndex === 0 && (
        <Box sx={{ display: 'flex', flexWrap: 'wrap', margin: 2, height: 100, justifyContent: 'flex-end', alignItems: 'center' }}>
          <input type="file" onChange={event => setGifUrl(URL.createObjectURL(event.target.files[0]))} /> 
        </Box>
      )}
      {tabIndex === 1 && (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center',  margin: 2, height: 100 }}>
          <TextField
            sx={{ marginTop: 2 }}
            value={gifUrl}
            onChange={handleGifUrlChange}
            label="or paste a GIF URL"
            variant="outlined"
            fullWidth
          />
        </Box>
      )}
      {tabIndex === 2 && (
        <div>
          <h3 style={{ textAlign: 'center' }}>
            GIF Preview
          </h3>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: 2 }}>
            <Box
              sx={{ width: 200, height: 200, border: '2px dashed grey' }}
              onDrop={handleGifDrop}
              onDragOver={(event) => event.preventDefault()}
            >
              {gifUrl ? <img src={gifUrl} style={{ width: 200, height: 200 }} alt="Dragged GIF" /> : 'Drag and drop a GIF here'}
            </Box>
          </Box>
        </div> 
      )}
      
      <Button onClick={handleSendGifUrl} variant="contained" sx={{ marginTop: 2, backgroundColor: '#47585F'}}>Load GIF</Button>
    </div>
  );
};

export default GifChooser;
