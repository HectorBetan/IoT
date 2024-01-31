import { createContext, useContext, useEffect, useState } from "react";
import { storage, auth, db } from "../firebase";
import axios from "axios";
import {
    signOut,
    onAuthStateChanged,
    GoogleAuthProvider,
    signInWithPopup,
    updateProfile,
    reauthenticateWithPopup,
    deleteUser,
} from "firebase/auth";
import { ref, getDownloadURL } from "firebase/storage";
import {
    doc,
    setDoc,
    updateDoc,
    getDoc,
    deleteDoc,
    arrayRemove,
    collection,
    getDocs,

} from "firebase/firestore";
const appContext = createContext();
export const useApp = () => {
    const context = useContext(appContext);
    if (!context) throw new Error("No hay contexto de autenticación");
    return context;
};
export function AppProvider({ children }) {
    const [loading, setLoading] = useState(true);
    const sensors = ["A458731", "A244453", "A250198", "A249310", "A350872"];
    const [aqidata, setAqiData] = useState([]);
    const [openMeteo, setOpenMeteo] = useState(null);
    
    const read = async () => {
        let sensor= [];
        
        for(let s in sensors){
            const response = await axios.get(`https://api.waqi.info/feed/${sensors[s]}/?token=ab7c393c9b0cd9ebb6d358fd88b31eb1edc62448`);
            
            if(response.data && response.data !== String){
                sensor[s] = response.data.data;
            }
            
        }
        const open = await axios.get(`https://air-quality-api.open-meteo.com/v1/air-quality?latitude=3.4372&longitude=-76.5225&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi,european_aqi&timezone=auto&forecast_days=1`);
        const openWeather = await axios.get(`https://api.openweathermap.org/data/2.5/weather?lat=3.4372&lon=-76.5225&appid=a7ec2db47ecdc404fb71cf396efab6a6`)
        console.log(openWeather)
        setOpenMeteo(open.data)
        setAqiData(sensor)
        
      };
    if (loading){
        read()
        setLoading(false)
    }
    
    return (
        <appContext.Provider
            value={{
                aqidata,
                openMeteo,
            }}
        >
            {children}
        </appContext.Provider>
    );
}
