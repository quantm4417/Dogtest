import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix Leaflet icon issue
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

interface MapProps {
  gpxUrl?: string;
}

export default function Map({ gpxUrl }: MapProps) {
  const [positions, setPositions] = useState<[number, number][]>([]);
  
  useEffect(() => {
    if (!gpxUrl) return;
    
    // Fetch and parse GPX
    fetch(gpxUrl)
      .then(res => res.text())
      .then(str => {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(str, "text/xml");
        const trkpts = xmlDoc.getElementsByTagName("trkpt");
        const latlngs: [number, number][] = [];
        
        for (let i = 0; i < trkpts.length; i++) {
            const lat = parseFloat(trkpts[i].getAttribute("lat") || "0");
            const lon = parseFloat(trkpts[i].getAttribute("lon") || "0");
            latlngs.push([lat, lon]);
        }
        setPositions(latlngs);
      })
      .catch(console.error);
  }, [gpxUrl]);

  if (!gpxUrl || positions.length === 0) {
     return <div className="h-64 bg-gray-100 flex items-center justify-center text-gray-400">No route data</div>;
  }

  const center = positions[0];

  return (
    <MapContainer center={center} zoom={13} style={{ height: '400px', width: '100%' }} className="rounded-lg z-0">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Polyline positions={positions} color="blue" />
      <Marker position={positions[0]}><Popup>Start</Popup></Marker>
      <Marker position={positions[positions.length - 1]}><Popup>End</Popup></Marker>
    </MapContainer>
  );
}

