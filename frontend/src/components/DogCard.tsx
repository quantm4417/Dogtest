import React from 'react';
import { Link } from 'react-router-dom';
import { Dog as DogIcon } from 'lucide-react';
import { Dog } from '../api/hooks';

interface DogCardProps {
  dog: Dog;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function DogCard({ dog }: DogCardProps) {
  const imageUrl = dog.avatar_image_url 
    ? (dog.avatar_image_url.startsWith('http') ? dog.avatar_image_url : `${API_URL}${dog.avatar_image_url}`)
    : null;

  return (
    <Link 
      to={`/dogs/${dog.id}`}
      className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow overflow-hidden flex flex-col"
    >
      <div className="h-48 bg-gray-100 relative">
        {imageUrl ? (
          <img 
            src={imageUrl} 
            alt={dog.name} 
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            <DogIcon size={64} />
          </div>
        )}
      </div>
      <div className="p-4 flex-1">
        <h3 className="text-xl font-bold text-gray-900">{dog.name}</h3>
        <p className="text-sm text-gray-500">{dog.breed || 'Unknown Breed'}</p>
        
        <div className="mt-4 flex gap-2 flex-wrap">
           {/* Quick stats or tags could go here */}
           <span className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded-full">
             {dog.sex === 'UNKNOWN' ? '?' : dog.sex}
           </span>
           {dog.weight_kg && (
             <span className="text-xs bg-green-50 text-green-700 px-2 py-1 rounded-full">
               {dog.weight_kg} kg
             </span>
           )}
        </div>
      </div>
    </Link>
  );
}

