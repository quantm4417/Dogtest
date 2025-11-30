import React, { useState } from 'react';
import { Plus, Bell, AlertTriangle } from 'lucide-react';
import { useDogs, useReminders, useCreateDog } from '../../api/hooks';
import DogCard from '../../components/DogCard';
import { format, parseISO, isPast } from 'date-fns';

export default function Dashboard() {
  const { data: dogs, isLoading: dogsLoading } = useDogs();
  const { data: reminders, isLoading: remindersLoading } = useReminders();
  const createDog = useCreateDog();
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newDogName, setNewDogName] = useState('');

  const handleCreateDog = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newDogName) return;
    await createDog.mutateAsync({ name: newDogName, sex: 'UNKNOWN' });
    setIsModalOpen(false);
    setNewDogName('');
  };

  if (dogsLoading || remindersLoading) return <div className="p-8">Loading...</div>;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Main Content: Dogs List */}
      <div className="lg:col-span-2">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">My Dogs</h1>
          <button 
            onClick={() => setIsModalOpen(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700 transition-colors"
          >
            <Plus size={20} /> Add Dog
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {dogs?.map((dog) => (
            <DogCard key={dog.id} dog={dog} />
          ))}
          
          {dogs?.length === 0 && (
             <div className="col-span-full text-center py-12 bg-white rounded-xl border border-dashed border-gray-300">
                <p className="text-gray-500 mb-4">No dogs added yet.</p>
                <button 
                  onClick={() => setIsModalOpen(true)}
                  className="text-blue-600 font-medium hover:underline"
                >
                  Add your first dog
                </button>
             </div>
          )}
        </div>
      </div>

      {/* Sidebar: Reminders */}
      <div className="lg:col-span-1">
        <div className="bg-white rounded-xl shadow-sm p-6 sticky top-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Bell size={20} /> Reminders
          </h2>
          
          <div className="space-y-4">
            {reminders?.length === 0 && (
               <p className="text-gray-400 text-sm">No upcoming tasks.</p>
            )}
            
            {reminders?.map((reminder) => (
              <div key={`${reminder.type}-${reminder.id}`} className="flex items-start gap-3 p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors border-l-4 border-blue-500">
                <div className="flex-1">
                  <div className="flex justify-between items-start">
                     <p className="font-medium text-gray-900">{reminder.title}</p>
                     {reminder.is_overdue && <AlertTriangle size={16} className="text-red-500" />}
                  </div>
                  <div className="flex justify-between text-xs mt-1 text-gray-500">
                    <span>{reminder.dog_name}</span>
                    <span className={reminder.is_overdue ? 'text-red-600 font-bold' : ''}>
                      {format(parseISO(reminder.date), 'MMM d')}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Simple Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-bold mb-4">Add New Dog</h3>
            <form onSubmit={handleCreateDog}>
              <input
                autoFocus
                type="text"
                placeholder="Dog Name"
                className="w-full border p-2 rounded mb-4"
                value={newDogName}
                onChange={(e) => setNewDogName(e.target.value)}
              />
              <div className="flex justify-end gap-2">
                <button 
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded"
                >
                  Cancel
                </button>
                <button 
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
