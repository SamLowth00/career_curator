<template>
    <div class="pb-4">
        <Pie :data="pieChartData" :options="chartOptions" />
        <p v-if="otherCount > 0" class="text-center text-sm font-semibold text-gray-400 mt-2">(+{{ otherCount }} other skills)</p>
    </div>
</template>

<script setup>
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'
import { Pie } from 'vue-chartjs'
import { ref, onMounted, computed } from 'vue'
import { getSkills } from '@/api/api';
ChartJS.register(Title, Tooltip, Legend, ArcElement)

const CHART_COLORS = [
  '#4E79A7', // blue
  '#F28E2B', // orange
  '#E15759', // red
  '#76B7B2', // teal
  '#59A14F', // green
  '#EDC948', // yellow
  '#B07AA1', // purple
  '#FF9DA7', // pink
  '#9C755F', // brown
  '#BAB0AC', // gray
  '#1F77B4', // bright blue
  '#FF7F0E', // bright orange
  '#2CA02C', // bright green
  '#D62728', // bright red
  '#9467BD', // bright purple
  '#8C564B', // warm brown
  '#E377C2', // magenta
  '#7F7F7F', // mid gray
  '#BCBD22', // olive
  '#17BECF'  // cyan
]

const skillsData = ref([]);
const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    },
    title: {
      display: true,
      text: 'My Skills',
      font: {
        size: 18
      }
    }
  }
}
const otherCount = computed(() => {
  const sorted = [...skillsData.value].sort((a, b) => b.job_count - a.job_count)
  return sorted.slice(5).length
})

const pieChartData = computed(() => {
  const sorted = [...skillsData.value].sort((a, b) => b.job_count - a.job_count)
  const top5 = sorted.slice(0, 5)
  const labels = top5.map((skill) => skill.name)
  const data = top5.map((skill) => skill.job_count)
  return {
    labels,
    datasets: [{
      label: 'Skill chart',
      data,
      backgroundColor: CHART_COLORS.slice(0, labels.length)
    }]
  }
})

async function getSkillsApi() {
    const response = await getSkills()
    console.log(response)
    skillsData.value = response
}
onMounted(() => {
    console.log('mounted')
    getSkillsApi();
})
</script>