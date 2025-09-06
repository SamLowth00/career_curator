<template>
    <div class="flex justify-center items-center min-h-[250px] max-h-[500px] overflow-scroll">
        <template v-if="fetchingPlan">
            <span>FETCHING PLAN</span>
        </template>
        <template v-else-if="!plan">
            <button @click="handleGenerate" class="bg-primary rounded p-4 flex gap-1 shadow-lg text-white cursor-pointer hover:bg-primary-hover">
                <img src="@/icons/plus-circle-white.svg" alt="Create Job" class="w-6 h-6" />
                Generate a new plan
            </button>
        </template>
        <template v-else>
            <div class="plan-container" v-html="marked(plan)"></div>
        </template>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { generatePlan } from '@/api/api';
import { marked } from 'marked';
const plan = ref('');
const fetchingPlan = ref(false)

async function handleGenerate () {
    fetchingPlan.value = true
    const response = await generatePlan();
    console.log('resp', response);
    plan.value = response;
    fetchingPlan.value = false
}

</script>

<style>
/* Container for the plan content */
.plan-container {
    max-width: 64rem; /* 1024px */
    margin: 0 auto;
    padding: 1.5rem;
}

/* Markdown content styling */
.plan-container h1 {
    font-size: 1.875rem; /* 30px */
    font-weight: 700;
    margin-bottom: 1rem;
    line-height: 1.2;
}

.plan-container h2 {
    font-size: 1.5rem; /* 24px */
    font-weight: 600;
    margin-bottom: 0.75rem;
    line-height: 1.3;
}

.plan-container h3 {
    font-size: 1.25rem; /* 20px */
    font-weight: 600;
    margin-bottom: 0.5rem;
    line-height: 1.4;
}

.plan-container p {
    margin-bottom: 1rem;
    line-height: 1.6;
}
.plan-container ul {
    margin-bottom: 1rem;
    padding-left: 1.5rem;
    list-style-type: disc; /* This adds the bullet points */
}

.plan-container ol {
    margin-bottom: 1rem;
    padding-left: 1.5rem;
    list-style-type: decimal; /* This adds numbers */
}

.plan-container li {
    margin-bottom: 0.25rem;
    display: list-item; /* Ensures list items display properly */
}

/* Nested lists */
.plan-container ul ul {
    list-style-type: circle; /* Different bullet for nested lists */
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
}

.plan-container ul ul ul {
    list-style-type: square; /* Square bullets for third level */
}

.plan-container ol ol {
    list-style-type: lower-alpha; /* Letters for nested ordered lists */
}

.plan-container li {
    margin-bottom: 0.25rem;
}

.plan-container a {
    color: #2563eb; /* blue-600 */
    text-decoration: underline;
}

.plan-container a:hover {
    color: #1e40af; /* blue-800 */
}

.plan-container code {
    background-color: #f3f4f6; /* gray-100 */
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.875rem;
    font-family: 'Courier New', Courier, monospace;
}

.plan-container pre {
    background-color: #f3f4f6; /* gray-100 */
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    margin-bottom: 1rem;
    font-family: 'Courier New', Courier, monospace;
}

.plan-container blockquote {
    border-left: 4px solid #d1d5db; /* gray-300 */
    padding-left: 1rem;
    font-style: italic;
    margin-bottom: 1rem;
}

/* Additional styling for better readability */
.plan-container strong {
    font-weight: 600;
}

.plan-container em {
    font-style: italic;
}

.plan-container hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 2rem 0;
}

.plan-container table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1rem;
}

.plan-container th,
.plan-container td {
    border: 1px solid #d1d5db;
    padding: 0.5rem;
    text-align: left;
}

.plan-container th {
    background-color: #f9fafb;
    font-weight: 600;
}
</style>

