import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDog } from '../../api/hooks';
import { 
  User, 
  Heart, 
  Brain, 
  Map, 
  CalendarCheck, 
  Package, 
  ArrowLeft 
} from 'lucide-react';

// Placeholder imports for tabs - I'll create them next
import ProfileTab from '../../components/dogs/ProfileTab';
import HealthTab from '../../components/dogs/HealthTab';
import TrainingTab from '../../components/dogs/TrainingTab';
import WalksTab from '../../components/dogs/WalksTab';
import CareTab from '../../components/dogs/CareTab';
import GearTab from '../../components/dogs/GearTab';

export default function DogDetail() {
  const { id } = useParams();
  const dogId = parseInt(id || '0');
  const { data: dog, isLoading } = useDog(dogId);
  const navigate = useNavigate();
  
  const [activeTab, setActiveTab] = useState<'profile' | 'health' | 'training' | 'walks' | 'care' | 'gear'>('profile');

  if (isLoading) return <div>Loading...</div>;
  if (!dog) return <div>Dog not found</div>;

  const tabs = [
    { id: 'profile', label: 'Profile', icon: <User size={18} /> },
    { id: 'health', label: 'Health', icon: <Heart size={18} /> },
    { id: 'training', label: 'Training', icon: <Brain size={18} /> },
    { id: 'walks', label: 'Walks', icon: <Map size={18} /> },
    { id: 'care', label: 'Care', icon: <CalendarCheck size={18} /> },
    { id: 'gear', label: 'Gear', icon: <Package size={18} /> },
  ] as const;

  return (
    <div>
      <button 
        onClick={() => navigate('/')}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
      >
        <ArrowLeft size={20} /> Back to Dashboard
      </button>

      <div className="bg-white rounded-xl shadow-sm overflow-hidden mb-6">
        <div className="h-32 bg-gradient-to-r from-blue-500 to-blue-600"></div>
        <div className="px-6 pb-6">
          <div className="flex items-end -mt-12 mb-6">
            <div className="w-24 h-24 bg-white rounded-full p-1 shadow-md">
              <div className="w-full h-full rounded-full bg-gray-200 overflow-hidden">
                {dog.avatar_image_url ? (
                  <img src={dog.avatar_image_url.startsWith('http') ? dog.avatar_image_url : `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${dog.avatar_image_url}`} alt={dog.name} className="w-full h-full object-cover" />
                ) : (
                  <User className="w-full h-full p-4 text-gray-400" />
                )}
              </div>
            </div>
            <div className="ml-4 mb-1">
              <h1 className="text-2xl font-bold text-gray-900">{dog.name}</h1>
              <p className="text-gray-500">{dog.breed}</p>
            </div>
          </div>

          <div className="flex border-b overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 border-b-2 font-medium whitespace-nowrap transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab.icon}
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="min-h-[400px]">
        {activeTab === 'profile' && <ProfileTab dog={dog} />}
        {activeTab === 'health' && <HealthTab dogId={dogId} />}
        {activeTab === 'training' && <TrainingTab dogId={dogId} />}
        {activeTab === 'walks' && <WalksTab dogId={dogId} />}
        {activeTab === 'care' && <CareTab dogId={dogId} />}
        {activeTab === 'gear' && <GearTab dogId={dogId} />}
      </div>
    </div>
  );
}
