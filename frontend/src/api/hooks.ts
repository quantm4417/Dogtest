import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './client';

// ... existing types ...
export interface Dog {
  id: number;
  name: string;
  breed?: string;
  date_of_birth?: string;
  sex: 'MALE' | 'FEMALE' | 'UNKNOWN';
  weight_kg?: number;
  avatar_image_url?: string;
  notes?: string;
  details?: DogProfileDetails;
}

export interface DogProfileDetails {
  id: number;
  dog_id: number;
  allergies?: string;
  forbidden_foods?: string;
  preferred_foods?: string;
  diagnosed_conditions?: string;
  care_notes?: string;
}

export interface VetVisit {
  id: number;
  dog_id: number;
  date: string;
  vet_name?: string;
  reason: string;
  diagnosis?: string;
  treatment_and_medication?: string;
  notes_markdown?: string;
}

export interface Vaccination {
  id: number;
  dog_id: number;
  date: string;
  vaccine_type: string;
  valid_until?: string;
  notes?: string;
}

export interface Equipment {
  id: number;
  dog_id: number;
  type: string;
  name: string;
  description?: string;
  purchase_date?: string;
  brand?: string;
  size?: string;
  notes?: string;
  is_active: boolean;
}

export interface Reminder {
  type: 'CARE_TASK' | 'VACCINATION' | 'VET_VISIT';
  id: number;
  date: string;
  title: string;
  dog_name: string;
  is_overdue: boolean;
}

export interface Walk {
    id: number;
    start_datetime: string;
    duration_minutes: number;
    mood: 'CALM' | 'NORMAL' | 'STRESSED';
    distance_km?: number;
    notes_markdown?: string;
    video_urls_json?: string[];
    gpx_file_url?: string;
    has_route_data: boolean;
}

export interface CareTask {
    id: number;
    title: string;
    interval_type: string;
    next_due_date: string;
    is_active: boolean;
}

export interface TrainingGoal {
    id: number;
    title: string;
    status: string;
    priority: number;
}

export interface BehaviorIssue {
    id: number;
    title: string;
    severity: number;
}

export interface TrainingLog {
    id: number;
    datetime: string;
    rating: number;
    notes_markdown?: string;
}

// Queries
export function useDogs() {
  return useQuery({
    queryKey: ['dogs'],
    queryFn: async () => {
      const { data } = await api.get<Dog[]>('/dogs/');
      return data;
    },
  });
}

export function useDog(id: number) {
  return useQuery({
    queryKey: ['dogs', id],
    queryFn: async () => {
      const { data } = await api.get<Dog>(`/dogs/${id}`);
      return data;
    },
    enabled: !!id,
  });
}

export function useDogDetails(id: number) {
    return useQuery({
        queryKey: ['dogs', id, 'details'],
        queryFn: async () => {
            const { data } = await api.get<DogProfileDetails>(`/dogs/${id}/details`);
            return data;
        },
        enabled: !!id
    });
}

export function useReminders() {
  return useQuery({
    queryKey: ['reminders'],
    queryFn: async () => {
      const { data } = await api.get<Reminder[]>('/reminders/upcoming');
      return data;
    },
  });
}

export function useVetVisits(dogId: number) {
    return useQuery({
        queryKey: ['health', 'vet-visits', dogId],
        queryFn: async () => {
            const { data } = await api.get<VetVisit[]>(`/health/vet-visits?dog_id=${dogId}`);
            return data;
        },
        enabled: !!dogId
    });
}

export function useVaccinations(dogId: number) {
    return useQuery({
        queryKey: ['health', 'vaccinations', dogId],
        queryFn: async () => {
            const { data } = await api.get<Vaccination[]>(`/health/vaccinations?dog_id=${dogId}`);
            return data;
        },
        enabled: !!dogId
    });
}

export function useEquipment(dogId: number) {
    return useQuery({
        queryKey: ['equipment', dogId],
        queryFn: async () => {
            const { data } = await api.get<Equipment[]>(`/equipment/?dog_id=${dogId}`);
            return data;
        },
        enabled: !!dogId
    });
}

export function useWalks(dogId?: number) {
    return useQuery({
        queryKey: ['walks', dogId],
        queryFn: async () => {
            const url = dogId ? `/walks/?dog_id=${dogId}` : '/walks/';
            const { data } = await api.get<Walk[]>(url);
            return data;
        },
    });
}

export function useCareTasks(dogId: number) {
    return useQuery({
        queryKey: ['care', 'tasks', dogId],
        queryFn: async () => {
            const { data } = await api.get<CareTask[]>(`/care/tasks?dog_id=${dogId}`);
            return data;
        },
    });
}

export function useTrainingGoals(dogId: number) {
    return useQuery({
        queryKey: ['training', 'goals', dogId],
        queryFn: async () => {
            const { data } = await api.get<TrainingGoal[]>(`/training/goals?dog_id=${dogId}`);
            return data;
        },
    });
}

export function useBehaviorIssues(dogId: number) {
    return useQuery({
        queryKey: ['training', 'issues', dogId],
        queryFn: async () => {
            const { data } = await api.get<BehaviorIssue[]>(`/training/issues?dog_id=${dogId}`);
            return data;
        },
    });
}

export function useTrainingLogs(dogId: number) {
    return useQuery({
        queryKey: ['training', 'logs', dogId],
        queryFn: async () => {
            const { data } = await api.get<TrainingLog[]>(`/training/logs?dog_id=${dogId}`);
            return data;
        },
    });
}

// Mutations
export function useCreateDog() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (newDog: Partial<Dog>) => {
      const { data } = await api.post('/dogs/', newDog);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dogs'] });
    },
  });
}

export function useUpdateDogDetails(dogId: number) {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (details: Partial<DogProfileDetails>) => {
            const { data } = await api.put(`/dogs/${dogId}/details`, details);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['dogs', dogId, 'details'] });
        }
    });
}

export function useUploadAvatar(dogId: number) {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (file: File) => {
            const formData = new FormData();
            formData.append('file', file);
            const { data } = await api.post(`/dogs/${dogId}/avatar`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            return data;
        },
        onSuccess: () => {
             queryClient.invalidateQueries({ queryKey: ['dogs', dogId] });
             queryClient.invalidateQueries({ queryKey: ['dogs'] });
        }
    });
}
