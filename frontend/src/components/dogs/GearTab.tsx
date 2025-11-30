import React from 'react';
import { useEquipment } from '../../api/hooks';
import { Plus, Package } from 'lucide-react';

export default function GearTab({ dogId }: { dogId: number }) {
  const { data: equipment, isLoading } = useEquipment(dogId);

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-bold flex items-center gap-2">
          <Package className="text-purple-600" /> Equipment
        </h3>
        <button className="text-sm bg-purple-50 text-purple-600 px-3 py-1 rounded-lg hover:bg-purple-100 flex items-center gap-1">
          <Plus size={16} /> Add Gear
        </button>
      </div>

      {isLoading ? <div>Loading...</div> : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {equipment?.length === 0 && <p className="text-gray-500 col-span-2">No equipment recorded.</p>}
          {equipment?.map((item) => (
            <div key={item.id} className="border border-gray-200 p-4 rounded-lg hover:border-purple-300 transition-colors">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-bold text-gray-900">{item.name}</h4>
                <span className="text-xs font-medium bg-gray-100 px-2 py-1 rounded text-gray-600">{item.type}</span>
              </div>
              {item.brand && <p className="text-sm text-gray-600 mb-1">Brand: {item.brand}</p>}
              {item.size && <p className="text-sm text-gray-600 mb-1">Size: {item.size}</p>}
              {!item.is_active && <span className="text-xs text-red-500 font-medium">Inactive</span>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

