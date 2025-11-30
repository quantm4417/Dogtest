import React from 'react';
import { useTrainingGoals, useBehaviorIssues, useTrainingLogs } from '../../api/hooks';
import { Brain, Plus, Target, AlertCircle, History } from 'lucide-react';
import { format, parseISO } from 'date-fns';

export default function TrainingTab({ dogId }: { dogId: number }) {
  const { data: goals } = useTrainingGoals(dogId);
  const { data: issues } = useBehaviorIssues(dogId);
  const { data: logs } = useTrainingLogs(dogId);

  return (
    <div className="space-y-8">
      
      {/* Goals & Issues Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl shadow-sm p-6">
             <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold flex items-center gap-2"><Target className="text-blue-600" /> Goals</h3>
                <button size={16} className="text-blue-600"><Plus /></button>
             </div>
             <div className="space-y-3">
                {goals?.length === 0 && <p className="text-sm text-gray-500">No goals set.</p>}
                {goals?.map(g => (
                    <div key={g.id} className="bg-gray-50 p-3 rounded flex justify-between">
                        <span>{g.title}</span>
                        <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">{g.status}</span>
                    </div>
                ))}
             </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6">
             <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold flex items-center gap-2"><AlertCircle className="text-red-600" /> Behavior Issues</h3>
                <button size={16} className="text-red-600"><Plus /></button>
             </div>
             <div className="space-y-3">
                {issues?.length === 0 && <p className="text-sm text-gray-500">No issues recorded.</p>}
                {issues?.map(i => (
                    <div key={i.id} className="bg-gray-50 p-3 rounded flex justify-between">
                        <span>{i.title}</span>
                        <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded">Severity: {i.severity}</span>
                    </div>
                ))}
             </div>
          </div>
      </div>

      {/* Recent Logs */}
      <div className="bg-white rounded-xl shadow-sm p-6">
         <div className="flex justify-between items-center mb-6">
            <h3 className="font-bold flex items-center gap-2"><History className="text-purple-600" /> Recent Training Logs</h3>
            <button className="text-sm bg-purple-50 text-purple-600 px-3 py-1 rounded hover:bg-purple-100 flex items-center gap-1">
                <Plus size={16} /> Log Session
            </button>
         </div>
         <div className="space-y-4">
            {logs?.length === 0 && <p className="text-gray-500">No training logs.</p>}
            {logs?.map(log => (
                <div key={log.id} className="border-b pb-4 last:border-0">
                   <div className="flex justify-between mb-2">
                      <span className="font-bold">{format(parseISO(log.datetime), 'MMM d, yyyy • HH:mm')}</span>
                      <span className="text-sm">Rating: {log.rating}/5</span>
                   </div>
                   {log.notes_markdown && <p className="text-gray-600 text-sm line-clamp-2">{log.notes_markdown}</p>}
                </div>
            ))}
         </div>
      </div>
    </div>
  );
}
