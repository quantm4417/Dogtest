import React from 'react';
import { useCareTasks } from '../../api/hooks';
import { CalendarCheck, Plus, CheckCircle } from 'lucide-react';
import { format, parseISO } from 'date-fns';

export default function CareTab({ dogId }: { dogId: number }) {
  const { data: tasks, isLoading } = useCareTasks(dogId);

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
       <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-bold flex items-center gap-2">
          <CalendarCheck className="text-orange-600" /> Care Routine
        </h3>
        <button className="text-sm bg-orange-50 text-orange-600 px-3 py-1 rounded-lg hover:bg-orange-100 flex items-center gap-1">
          <Plus size={16} /> Add Task
        </button>
      </div>

      {isLoading ? <div>Loading...</div> : (
        <div className="space-y-4">
          {tasks?.length === 0 && <p className="text-gray-500">No care tasks.</p>}
          {tasks?.map((task) => (
            <div key={task.id} className="border border-gray-200 p-4 rounded-lg flex items-center justify-between">
                <div>
                   <h4 className="font-bold text-gray-900">{task.title}</h4>
                   <p className="text-sm text-gray-600">Due: {format(parseISO(task.next_due_date), 'MMM d, yyyy')}</p>
                   <p className="text-xs text-gray-400 mt-1">Repeats: {task.interval_type}</p>
                </div>
                <button className="text-gray-400 hover:text-green-600 transition-colors" title="Mark Complete">
                    <CheckCircle size={24} />
                </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
