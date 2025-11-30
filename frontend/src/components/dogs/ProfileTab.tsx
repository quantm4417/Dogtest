import React, { useState, useEffect } from 'react';
import { Dog, useDogDetails, useUpdateDogDetails, useUploadAvatar } from '../../api/hooks';
import { Upload, Save } from 'lucide-react';

export default function ProfileTab({ dog }: { dog: Dog }) {
  const { data: details, isLoading } = useDogDetails(dog.id);
  const updateDetails = useUpdateDogDetails(dog.id);
  const uploadAvatar = useUploadAvatar(dog.id);
  
  const [formData, setFormData] = useState({
    allergies: '',
    forbidden_foods: '',
    preferred_foods: '',
    diagnosed_conditions: '',
    care_notes: ''
  });

  useEffect(() => {
    if (details) {
      setFormData({
        allergies: details.allergies || '',
        forbidden_foods: details.forbidden_foods || '',
        preferred_foods: details.preferred_foods || '',
        diagnosed_conditions: details.diagnosed_conditions || '',
        care_notes: details.care_notes || ''
      });
    }
  }, [details]);

  const handleSave = async () => {
    await updateDetails.mutateAsync(formData);
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      await uploadAvatar.mutateAsync(e.target.files[0]);
    }
  };

  if (isLoading) return <div>Loading details...</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div className="md:col-span-2 space-y-6">
        <div className="bg-white p-6 rounded-xl shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-bold">Profile Details</h3>
            <button 
              onClick={handleSave}
              disabled={updateDetails.isPending}
              className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              <Save size={18} /> {updateDetails.isPending ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Allergies</label>
              <textarea
                className="w-full border rounded-md p-2 h-24"
                placeholder="List any allergies..."
                value={formData.allergies}
                onChange={e => setFormData({...formData, allergies: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Forbidden Foods</label>
              <textarea
                className="w-full border rounded-md p-2 h-24"
                placeholder="What shouldn't they eat?"
                value={formData.forbidden_foods}
                onChange={e => setFormData({...formData, forbidden_foods: e.target.value})}
              />
            </div>
            <div>
               <label className="block text-sm font-medium text-gray-700 mb-1">Diagnosed Conditions</label>
               <textarea
                className="w-full border rounded-md p-2 h-24"
                placeholder="Chronic issues or past diagnoses..."
                value={formData.diagnosed_conditions}
                onChange={e => setFormData({...formData, diagnosed_conditions: e.target.value})}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        <div className="bg-white p-6 rounded-xl shadow-sm">
          <h3 className="text-lg font-bold mb-4">Avatar</h3>
          <div className="flex flex-col items-center">
             <div className="w-32 h-32 bg-gray-100 rounded-full mb-4 overflow-hidden relative group">
               {dog.avatar_image_url ? (
                 <img 
                    src={dog.avatar_image_url.startsWith('http') ? dog.avatar_image_url : `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${dog.avatar_image_url}`} 
                    alt="Avatar" 
                    className="w-full h-full object-cover" 
                 />
               ) : (
                 <div className="w-full h-full flex items-center justify-center text-gray-400">No Image</div>
               )}
               
               <label className="absolute inset-0 bg-black/50 flex items-center justify-center text-white opacity-0 group-hover:opacity-100 cursor-pointer transition-opacity">
                 <Upload size={24} />
                 <input type="file" className="hidden" accept="image/*" onChange={handleFileChange} />
               </label>
             </div>
             <p className="text-sm text-gray-500">Click image to upload new photo</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm">
           <h3 className="text-lg font-bold mb-4">Quick Notes</h3>
           <div className="text-sm text-gray-600">
             <p><strong>Born:</strong> {dog.date_of_birth || 'Unknown'}</p>
             <p><strong>Sex:</strong> {dog.sex}</p>
             <p><strong>Weight:</strong> {dog.weight_kg ? `${dog.weight_kg} kg` : 'Unknown'}</p>
           </div>
        </div>
      </div>
    </div>
  );
}

