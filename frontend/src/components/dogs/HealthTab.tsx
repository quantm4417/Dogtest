import React from 'react';
import { useVetVisits, useVaccinations } from '../../api/hooks';
import { Plus, FileText, Syringe } from 'lucide-react';
import { format, parseISO } from 'date-fns';

export default function HealthTab({ dogId }: { dogId: number }) {
  const { data: visits, isLoading: visitsLoading } = useVetVisits(dogId);
  const { data: vaxs, isLoading: vaxsLoading } = useVaccinations(dogId);

  return (
    <div className="space-y-8">
      {/* Vet Visits Section */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-bold flex items-center gap-2">
            <FileText className="text-blue-600" /> Vet Visits
          </h3>
          <button className="text-sm bg-blue-50 text-blue-600 px-3 py-1 rounded-lg hover:bg-blue-100 flex items-center gap-1">
            <Plus size={16} /> Add Visit
          </button>
        </div>

        {visitsLoading ? <div>Loading...</div> : (
          <div className="space-y-4">
            {visits?.length === 0 && <p className="text-gray-500">No vet visits recorded.</p>}
            {visits?.map((visit) => (
              <div key={visit.id} className="border-l-4 border-blue-500 bg-gray-50 p-4 rounded-r-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-bold text-gray-900">{visit.reason}</h4>
                    <p className="text-sm text-gray-600">Vet: {visit.vet_name || 'Unknown'}</p>
                    {visit.diagnosis && (
                      <p className="mt-2 text-sm"><span className="font-semibold">Diagnosis:</span> {visit.diagnosis}</p>
                    )}
                  </div>
                  <span className="text-sm font-medium text-gray-500">
                    {format(parseISO(visit.date), 'MMM d, yyyy')}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Vaccinations Section */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-bold flex items-center gap-2">
            <Syringe className="text-green-600" /> Vaccinations
          </h3>
          <button className="text-sm bg-green-50 text-green-600 px-3 py-1 rounded-lg hover:bg-green-100 flex items-center gap-1">
            <Plus size={16} /> Add Vaccine
          </button>
        </div>

        {vaxsLoading ? <div>Loading...</div> : (
          <div className="space-y-4">
            {vaxs?.length === 0 && <p className="text-gray-500">No vaccinations recorded.</p>}
            {vaxs?.map((vax) => (
              <div key={vax.id} className="border border-gray-200 p-4 rounded-lg flex justify-between items-center">
                <div>
                  <h4 className="font-bold text-gray-900">{vax.vaccine_type}</h4>
                  <p className="text-sm text-gray-500">Given: {format(parseISO(vax.date), 'MMM d, yyyy')}</p>
                </div>
                <div className="text-right">
                  {vax.valid_until && (
                    <p className="text-sm">
                      Expires: <span className="font-medium text-gray-900">{format(parseISO(vax.valid_until), 'MMM d, yyyy')}</span>
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

