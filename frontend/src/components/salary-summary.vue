<template>
<div class="p-6 h-full flex flex-col justify-center items-center">
    <div class="text-center">
    <h3 class="text-lg font-semibold text-gray-700 mb-2">Average Salary</h3>
    <div class="text-4xl font-bold text-green-600 mb-1">
        {{ aveSalary.avg_salary ? `£${aveSalary.avg_salary}` : '--' }}
    </div>
    <p class="text-sm text-gray-500">{{ salaryText }}</p>
    </div>
</div>
</template>

<script setup>
import { getAverageSalary } from '@/api/api';
import { onMounted, ref, computed } from 'vue';
const aveSalary = ref({})
const getSalaryData = async () => {
    const salary = await getAverageSalary()
    console.log('salary', salary);
    aveSalary.value = salary;
}
const salaryText = computed(() => {
    return aveSalary.value?.avg_salary ?
        `Based on ${aveSalary.value.records_used} jobs with salaries` :
        'Add some jobs with salaries to see the rundown'
})

onMounted(() => {
    getSalaryData()
})
</script>

<style>
/* Additional custom styles if needed */
</style>