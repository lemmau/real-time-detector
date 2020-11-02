import React from 'react';
import { Navbar } from '../components/ui/Navbar';
import { Switch, Route, Redirect } from 'react-router-dom';

import { ConfigurationScreen } from '../components/configuration/ConfigurationScreen';
import { StatisticsScreen } from '../components/statistics/StatisticsScreen';
import { CameraScreen } from '../components/camera/CameraScreen';
import { WebcamScreen } from '../components/webcam/WebcamScreen';
import { ToastProvider } from 'react-toast-notifications'

export const DashboardRoutes = () => {
    return (
        <>
            <Navbar />
            
            <div className="container mt-2">
                <Switch>
                    <Route exact path="/configuration" component={ ConfigurationScreen } />
                    <Route exact path="/statistics" component={ StatisticsScreen } />
                    <Route exact path="/camera" component={ CameraScreen } />
                    <ToastProvider>
                    <Route exact path="/webcam" component={ WebcamScreen } />
                    </ToastProvider>

                    <Redirect to="/camera" />
                </Switch>
            </div>
        </>
    )
}
