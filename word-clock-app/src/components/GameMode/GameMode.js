import React, { useState } from 'react';
import { Button, IconButton } from '@mui/material';
import ArrowCircleLeftIcon from '@mui/icons-material/ArrowCircleLeft';
import ArrowCircleDownSharpIcon from '@mui/icons-material/ArrowCircleDownSharp';
import ArrowCircleRightIcon from '@mui/icons-material/ArrowCircleRight';
import ArrowCircleUpIcon from '@mui/icons-material/ArrowCircleUp';

import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import RefreshIcon from '@mui/icons-material/Refresh';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';

import "./GameMode.css";

const GameMode = () => {


    const handleButtonClick = async (buttonName) => {
      console.log(buttonName);
      const response = await fetch(`/game/${buttonName}`);
      const data = await response.json();
      console.log(data);
    };
  
  
    return (
      <div className='div-game-mode'>
        <div className='div-up'>
            <IconButton className='game-button' size='large' variant="contained" onClick={() => handleButtonClick('up')}>
              <ArrowCircleUpIcon style={{fontSize: 60}}/>
            </IconButton>
        </div>
        <div className='div-left-right'>
          <div className='div-left'>
            <IconButton className='game-button-hor' variant="contained" onClick={() => handleButtonClick('left')}>
              <ArrowCircleLeftIcon style={{fontSize: 60}}/>
            </IconButton>
          </div>
          <div className='div-right'>
            <IconButton className='game-button-hor' variant="contained" onClick={() => handleButtonClick('right')}>
              <ArrowCircleRightIcon style={{fontSize: 60}}/>
            </IconButton>
          </div>
            
        </div>
        <div className='div-down'>
            <IconButton className='game-button' variant="contained" onClick={() => handleButtonClick('down')}>
              <ArrowCircleDownSharpIcon style={{fontSize: 60}}/>
            </IconButton>
        </div>
        <div className='div-restart-exit'>
            <Button className='game-button' variant="contained" onClick={() => handleButtonClick('restart')} style={{margin: 10}} sx={{ backgroundColor: '#47585F' }}>
              <RefreshIcon />
            </Button>
            <Button className='game-button' variant="contained" onClick={() => handleButtonClick('exit')} style={{margin: 10}} sx={{ backgroundColor: '#47585F' }}>
              <ExitToAppIcon />
            </Button>
        </div>
      </div>
    );
  }
  
  export default GameMode;