import React, { useState } from 'react';
import { useWalks, Walk } from '../../api/hooks';
import { Map as MapIcon, Clock, Activity, Plus, ChevronDown, ChevronUp } from 'lucide-react';
import { format, parseISO } from 'date-fns';
import Map from '../Map';

export default function WalksTab({ dogId }: { dogId: number }) {
  const { data: walks, isLoading } = useWalks(dogId);
  const [expandedWalkId, setExpandedWalkId] = useState<number | null>(null);

  const toggleExpand = (id: number) => {
    if (expandedWalkId === id) setExpandedWalkId(null);
    else setExpandedWalkId(id);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
       <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-bold flex items-center gap-2">
          <MapIcon className="text-green-600" /> Walks History
        </h3>
        <button className="text-sm bg-green-50 text-green-600 px-3 py-1 rounded-lg hover:bg-green-100 flex items-center gap-1">
          <Plus size={16} /> Log Walk
        </button>
      </div>

      {isLoading ? <div>Loading...</div> : (
        <div className="space-y-4">
          {walks?.length === 0 && <p className="text-gray-500">No walks recorded.</p>}
          {walks?.map((walk) => (
            <div key={walk.id} className="border border-gray-200 rounded-lg overflow-hidden">
               <div 
                 className="p-4 flex items-center justify-between cursor-pointer hover:bg-gray-50"
                 onClick={() => toggleExpand(walk.id)}
               >
                  <div className="flex items-center gap-4">
                    <div className={`p-2 rounded-full ${
                        walk.mood === 'CALM' ? 'bg-green-100 text-green-600' :
                        walk.mood === 'STRESSED' ? 'bg-red-100 text-red-600' :
                        'bg-blue-100 text-blue-600'
                    }`}>
                       <Activity size={20} />
                    </div>
                    <div>
                       <h4 className="font-bold text-gray-900">{format(parseISO(walk.start_datetime), 'MMM d, yyyy • HH:mm')}</h4>
                       <div className="flex gap-3 text-sm text-gray-500">
                          <span className="flex items-center gap-1"><Clock size={14} /> {walk.duration_minutes} min</span>
                          {walk.distance_km && <span>{walk.distance_km} km</span>}
                       </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                     {walk.has_route_data && <span className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded">GPX</span>}
                     {expandedWalkId === walk.id ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                  </div>
               </div>
               
               {expandedWalkId === walk.id && (
                 <div className="p-4 border-t bg-gray-50">
                    {walk.notes_markdown && (
                      <div className="mb-4 text-gray-700 whitespace-pre-wrap">{walk.notes_markdown}</div>
                    )}
                    
                    {walk.gpx_file_url && (
                       <div className="mt-4 h-[400px] rounded-lg overflow-hidden border">
                          <Map gpxUrl={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${walk.gpx_file_url}`} />
                       </div>
                    )}
                 </div>
               )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
