<template>
  <div class="mt-6 bg-white rounded-xl shadow-lg border border-stone-200 overflow-hidden">
    <div class="px-6 py-4 bg-stone-50 border-b border-stone-200">
      <h3 class="text-lg font-semibold text-gray-900">My Skills</h3>
      <p class="text-sm text-gray-500 mt-1">Skills you already know — used to improve job skill extraction</p>
    </div>

    <div class="p-6">
      <!-- Loading state -->
      <div v-if="loadingSkills" class="text-sm text-gray-400">Loading skills...</div>

      <!-- Skill list -->
      <div v-else>
        <div v-if="userSkills.length === 0 && !showAddForm" class="text-sm text-gray-400 mb-4">
          No skills added yet.
        </div>

        <div v-for="skill in userSkills" :key="skill.id" class="mb-3">
          <!-- Edit mode -->
          <div v-if="editingId === skill.id" class="border border-stone-200 rounded-lg p-4 bg-stone-50 space-y-3">
            <input
              v-model="editForm.name"
              type="text"
              placeholder="Skill name"
              class="w-full border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <textarea
              v-model="editForm.description"
              placeholder="Short description (optional)"
              rows="2"
              class="w-full border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary resize-none"
            />
            <select
              v-model="editForm.level"
              class="border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option :value="null">Level: Unset</option>
              <option :value="1">Beginner</option>
              <option :value="2">Intermediate</option>
              <option :value="3">Expert</option>
            </select>
            <div class="flex gap-2">
              <button
                @click="saveEdit(skill.id)"
                :disabled="savingEdit"
                class="px-4 py-2 bg-primary text-white rounded-lg text-sm hover:bg-primary-hover disabled:opacity-50"
              >
                {{ savingEdit ? 'Saving...' : 'Save' }}
              </button>
              <button
                @click="cancelEdit"
                class="px-4 py-2 bg-stone-200 text-gray-700 rounded-lg text-sm hover:bg-stone-300"
              >
                Cancel
              </button>
            </div>
          </div>

          <!-- Display mode -->
          <div v-else class="flex items-start justify-between border border-stone-200 rounded-lg px-4 py-3 hover:bg-stone-50 transition-colors">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="font-medium text-gray-900 text-sm">{{ skill.name }}</span>
                <span
                  v-if="skill.level"
                  class="text-xs px-2 py-0.5 rounded-full font-medium"
                  :class="levelBadgeClass(skill.level)"
                >
                  {{ levelLabel(skill.level) }}
                </span>
              </div>
              <p v-if="skill.description" class="text-xs text-gray-500 mt-0.5">{{ skill.description }}</p>
            </div>
            <div class="flex items-center gap-2 ml-3 flex-shrink-0">
              <button @click="startEdit(skill)" class="text-xs text-gray-400 hover:text-gray-600">Edit</button>
              <button @click="removeSkill(skill.id)" class="text-xs text-red-400 hover:text-red-600">Delete</button>
            </div>
          </div>
        </div>

        <!-- Add skill form -->
        <div v-if="showAddForm" class="mt-3 border border-stone-200 rounded-lg p-4 bg-stone-50 space-y-3">
          <input
            v-model="addForm.name"
            type="text"
            placeholder="Skill name"
            class="w-full border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <textarea
            v-model="addForm.description"
            placeholder="Short description (optional)"
            rows="2"
            class="w-full border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary resize-none"
          />
          <select
            v-model="addForm.level"
            class="border border-stone-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option :value="null">Level: Unset</option>
            <option :value="1">Beginner</option>
            <option :value="2">Intermediate</option>
            <option :value="3">Expert</option>
          </select>
          <div class="flex gap-2">
            <button
              @click="submitAdd"
              :disabled="savingAdd || !addForm.name.trim()"
              class="px-4 py-2 bg-primary text-white rounded-lg text-sm hover:bg-primary-hover disabled:opacity-50"
            >
              {{ savingAdd ? 'Adding...' : 'Add Skill' }}
            </button>
            <button
              @click="cancelAdd"
              class="px-4 py-2 bg-stone-200 text-gray-700 rounded-lg text-sm hover:bg-stone-300"
            >
              Cancel
            </button>
          </div>
        </div>

        <!-- Add button -->
        <button
          v-if="!showAddForm"
          @click="showAddForm = true"
          class="mt-3 text-sm text-primary hover:text-primary-hover font-medium"
        >
          + Add a skill
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUserSkills, createUserSkill, updateUserSkill, deleteUserSkill } from '@/api/api.js'

const userSkills = ref([])
const loadingSkills = ref(true)

const showAddForm = ref(false)
const savingAdd = ref(false)
const addForm = ref({ name: '', description: '', level: null })

const editingId = ref(null)
const savingEdit = ref(false)
const editForm = ref({ name: '', description: '', level: null })

async function fetchSkills() {
  loadingSkills.value = true
  try {
    userSkills.value = await getUserSkills()
  } catch (error) {
    console.error('Failed to load user skills', error)
  } finally {
    loadingSkills.value = false
  }
}

async function submitAdd() {
  if (!addForm.value.name.trim()) return
  savingAdd.value = true
  try {
    const created = await createUserSkill({
      name: addForm.value.name.trim(),
      description: addForm.value.description || null,
      level: addForm.value.level,
    })
    userSkills.value.push(created)
    cancelAdd()
  } catch (error) {
    console.error('Failed to add skill', error)
  } finally {
    savingAdd.value = false
  }
}

function cancelAdd() {
  showAddForm.value = false
  addForm.value = { name: '', description: '', level: null }
}

function startEdit(skill) {
  editingId.value = skill.id
  editForm.value = { name: skill.name, description: skill.description || '', level: skill.level }
}

async function saveEdit(id) {
  savingEdit.value = true
  try {
    const updated = await updateUserSkill(id, {
      name: editForm.value.name.trim(),
      description: editForm.value.description || null,
      level: editForm.value.level,
    })
    const idx = userSkills.value.findIndex(s => s.id === id)
    if (idx !== -1) userSkills.value[idx] = updated
    cancelEdit()
  } catch (error) {
    console.error('Failed to update skill', error)
  } finally {
    savingEdit.value = false
  }
}

function cancelEdit() {
  editingId.value = null
  editForm.value = { name: '', description: '', level: null }
}

async function removeSkill(id) {
  try {
    await deleteUserSkill(id)
    userSkills.value = userSkills.value.filter(s => s.id !== id)
  } catch (error) {
    console.error('Failed to delete skill', error)
  }
}

function levelLabel(level) {
  return { 1: 'Beginner', 2: 'Intermediate', 3: 'Expert' }[level] || ''
}

function levelBadgeClass(level) {
  return {
    1: 'bg-blue-100 text-blue-700',
    2: 'bg-yellow-100 text-yellow-700',
    3: 'bg-green-100 text-green-700',
  }[level] || ''
}

onMounted(fetchSkills)
</script>
