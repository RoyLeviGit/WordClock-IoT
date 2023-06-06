import React from 'react';
import { useState } from 'react';
import { Grid, IconButton, Typography } from '@mui/material';
import AbcIcon from '@mui/icons-material/Abc';
import SportsCricketIcon from '@mui/icons-material/SportsCricket';
import AddReactionIcon from '@mui/icons-material/AddReaction';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import Looks6Icon from '@mui/icons-material/Looks6';


import WorldClock from '../WorldClock/WorldClock';
import GameMode from '../GameMode/GameMode';
import GameModePong from '../GameModePong/GameModePong';
import GifLamp from '../GifLamp/GifLamp';
import ColorPalette from '../ColorPalette/ColorPalette';
import "./AppMenu.css";

const AppMenu = () => {
    const [featureComponent, setFeatureComponent] = useState('');

    function fetchDigitalClock() {
        fetch('/digital-clock')
          .then(response => response.json())
          .then(data => {
            // Handle the response data
            console.log(data);
          })
          .catch(error => {
            // Handle any errors
            console.error(error);
          });
      }
      
    function fetchWordClock() {
        fetch('/word-clock')
            .then(response => response.json())
            .then(data => {
            // Handle the response data
            console.log(data);
            })
            .catch(error => {
            // Handle any errors
            console.error(error);
            });
        }
    function fetchGame(game) {
        fetch(`/${game}`)
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
    
    const updateFeatureComponent = (component) => {
        setFeatureComponent(component);
  };
    const componentLoader = () => {   
        if(featureComponent === 'Word Clock') {
           fetchWordClock();
           return (
            <div style={{display: 'flex', alignItems: 'center', flexDirection: 'column'}}>
                <h2 >
                    Word Clock
                </h2>
                <ColorPalette/>
                <WorldClock/>
            </div>
           )
        }
        else if(featureComponent === 'Digital Clock') {
            fetchDigitalClock();
            return (
                <div style={{display: 'flex', alignItems: 'center', flexDirection: 'column'}}>
                <h2 >
                    Digital Clock
                </h2>
                <ColorPalette/>
                <WorldClock/>
            </div>
               )
        }
        else if(featureComponent === 'Pong') {
            fetchGame(featureComponent === 'Pong'? "pong-game" : "snake-game");
            return (
                <GameModePong updateFeatureComponent={updateFeatureComponent} fetchWordClock={fetchWordClock}/>
            )
        }
        else if(featureComponent === 'Snake') {
            fetchGame(featureComponent === 'Pong'? "pong-game" : "snake-game");
            return (
                <GameMode updateFeatureComponent={updateFeatureComponent} fetchWordClock={fetchWordClock} />
                )
        }
        else if(featureComponent === 'Gif Lamp') {
            return (
                <GifLamp/>
            )
        }
        return null; // Add a default return statement outside of the if-else block
    };
      


    return (
    <div>
        <Grid container spacing={2} className="app-menu-container">
          <Grid item xs={4} className="app-menu-item">
            <IconButton aria-label="Word Clock" onClick={() => setFeatureComponent('Word Clock')}>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>    
                    <AbcIcon className="app-menu-icon" style={{ fontSize: 50 }} />
                    <span className="app-menu-label" style={{ fontSize: 14 }}>Word Clock</span>
                </div>
            </IconButton>
          </Grid>
          <Grid item xs={4} className="app-menu-item">
            <IconButton aria-label="Digital Clock" onClick={() => setFeatureComponent('Digital Clock')}>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>    
                    <Looks6Icon className="app-menu-icon" style={{ fontSize: 50 }} />
                    <span className="app-menu-label" style={{ fontSize: 14 }}>Digital Clock</span>
                </div>
            </IconButton>
          </Grid>
          <Grid item xs={4} className="app-menu-item">
            <IconButton aria-label="Pong Game" onClick={() => setFeatureComponent('Pong')}>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <SportsCricketIcon className="app-menu-icon" style={{ fontSize: 50 }} />
                <span className="app-menu-label" style={{ fontSize: 14 }}>Pong Game</span>
              </div>
            </IconButton>
          </Grid>
          <Grid item xs={4} className="app-menu-item">
            <IconButton aria-label="Snake Game" onClick={() => setFeatureComponent('Snake')}>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>        
                    <ShowChartIcon className="app-menu-icon" style={{ fontSize: 50 }} />
                    <span className="app-menu-label" style={{ fontSize: 14 }}>Snake Game</span>
                </div>
            </IconButton>
          </Grid>
          <Grid item xs={4} className="app-menu-item">
            <IconButton aria-label="Gif Lamp" onClick={() => setFeatureComponent('Gif Lamp')}>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>        
                    <AddReactionIcon className="app-menu-icon" style={{ fontSize: 50 }} />
                    <span className="app-menu-label" style={{ fontSize: 14 }}>Gif Lamp</span>
                </div>
            </IconButton>
          </Grid>
        </Grid>

        {componentLoader()}
    </div>
    );
};

export default AppMenu;
