import { useApp } from "../context/AppContext";
import { useState } from "react";
const Inicio = () => {
    const { aqidata, openMeteo } = useApp()
    function obtenerPosicionHora(arrayDeHoras) {
        // Obtén la hora actual en formato 'HH:mm'
        const fechaActual = new Date();

  // Formatea la fecha con minutos en '00'
  const horaActual = `${fechaActual.getFullYear()}-${(fechaActual.getMonth() + 1).toString().padStart(2, '0')}-${fechaActual.getDate().toString().padStart(2, '0')}T${fechaActual.getHours().toString().padStart(2, '0')}:00`;
        console.log(horaActual)
        // Encuentra la posición en el array que coincide con la hora actual
        const posicion = arrayDeHoras.findIndex(hora => hora === horaActual);
      
        return posicion;
    }
    const OpenMeteo = () => {
        if(openMeteo){
            let y = obtenerPosicionHora(openMeteo.hourly.time)
            console.log(y)
            return(
                <div>
                    <p>Fecha y Hora: {openMeteo.hourly.time[y]}</p>
                    <p>Latitud: {openMeteo.latitude}</p>
                    <p>Longitud: {openMeteo.longitude}</p>
                    <p>Zona horaria: {openMeteo.timezone}</p>
                    <p>Contaminantes:</p>
                    <ul className="list-unstyled">
                        <li>PM2.5: {openMeteo.hourly.pm2_5[y]}</li>
                        <li>PM10: {openMeteo.hourly.pm10[y]}</li>
                        <li>SO2: {openMeteo.hourly.sulphur_dioxide[y]}</li>
                        <li>NO2: {openMeteo.hourly.nitrogen_dioxide[y]}</li>
                        <li>CO: {openMeteo.hourly.carbon_monoxide[y]}</li>
                        <li>O3: {openMeteo.hourly.ozone[y]}</li>
                        
                    </ul>
                    <p>Air Quality Index:</p>
                    <ul className="list-unstyled">
                        <li>AQI: {openMeteo.hourly.us_aqi[y]}</li>
                        <li>CAQI: {openMeteo.hourly.european_aqi[y]}</li>
                    </ul>
                </div>
            )
        }
    }
    const Data = () =>{
        if(openMeteo){
            console.log(openMeteo)
        }
        let x = 0;
        if(aqidata){
            return(<div className="m-2 accordion" id="accordionsensor">
                {
                    
                    aqidata.map((sensor,i)=>{
                        
                        if(typeof sensor !== "string"){
                            x = x+1;
                            return(
                                <div className="accordion-item m-1"  key={i}>
                                    <h2 className="accordion-header">
                                    <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target={`#collapse-sensor${i}`} aria-expanded="true" aria-controls="collapseOne">
                                        Sensor {x}
                                    </button>
                                    </h2>
                                    
                                <div id={`collapse-sensor${i}`} className="accordion-collapse collapse" data-bs-parent="#accordionsensor">
                                <div className="accordion-body">
                                <div className="card p-3 mb-3">
                                <p className="mb-3">Índice AQI: {sensor.aqi}</p>
                                <div className="mb-3">
                                    <h5>Ciudad:</h5>
                                    <ul className="list-unstyled">
                                        <li>Nombre: {sensor.city.name}</li>
                                        <li>Ubicación: {sensor.city.location}</li>
                                        <li>Geo: {sensor.city.geo.join(', ')}</li>
                                        <li>URL: <a href={sensor.city.url} target="_blank" rel="noopener noreferrer">{sensor.city.url}</a></li>
                                    </ul>
                                </div>
                                <p>Índice dominante de contaminante: {sensor.dominentpol}</p>
                                <p>Índice IAQI PM2.5: {sensor.iaqi.pm25.v}</p>
                                <p>Índice: {sensor.idx}</p>
                                <div className="mb-3">
                                    <h5>Fecha y hora:</h5>
                                    <ul className="list-unstyled">
                                        <li>ISO: {sensor.time.iso}</li>
                                        <li>S: {sensor.time.s}</li>
                                        <li>Zona horaria: {sensor.time.tz}</li>
                                        <li>Valor V: {sensor.time.v}</li>
                                    </ul>
                                </div>
                                <hr />
                                </div>
                                    </div>
                                </div>
                            </div>
                            )
                            
                        } else {
                            return null
                        }
                        
                    })
                }
                        </div>)
        }
        
    }
   return(
    <div>
        <div className="m-3 accordion" id="accordionOpen">
            <div className="accordion-item">
                <h2 className="accordion-header">
                <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse1" aria-expanded="true" aria-controls="collapse1">
                    Open-Meteo
                </button>
                </h2>
                                    
                <div id="collapse1" className="accordion-collapse collapse show" data-bs-parent="#accordionOpen">
                    <div className="accordion-body">
                        <OpenMeteo></OpenMeteo>
                    </div>
                </div>
            </div>    
            <div className="accordion-item">
                <h2 className="accordion-header">
                <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse2" aria-expanded="true" aria-controls="collapse2">
                    aqicn service
                </button>
                </h2>
                                    
                <div id="collapse2" className="accordion-collapse collapse" data-bs-parent="#accordionaqicn">
                    <div className="accordion-body">
                        <Data></Data>
                    </div>
                </div>
            </div>   
        </div>
    </div>
   )

}
export default Inicio;