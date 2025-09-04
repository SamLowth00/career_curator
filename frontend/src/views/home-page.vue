<template>
    <div class="grid grid-cols-12 gap-4 p-5">
        <div class="col-span-12 rounded bg-white shadow-xl border-2 border-gray-300 transition-all duration-300 ease-in-out overflow-hidden" v-auto-animate>
            <PlanGeneratorWrapper />
        </div>
        <div class="col-span-6 rounded bg-white shadow-xl border-2 border-gray-300 transition-all duration-300 ease-in-out overflow-hidden">
            <SkillPieChart />
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import PlanGeneratorWrapper from '@/components/plan-generator-wrapper.vue';
import SkillPieChart from '@/components/skill-pie-chart.vue';
const router = useRouter()
const val = ref(false);

function goToCreateJob() {
  router.push('/create-job')
}
function goToJobsList() {
  router.push('/jobs-list')
}
function handleVal () {
    val.value = !val.value
}
</script>

<style>
</style>