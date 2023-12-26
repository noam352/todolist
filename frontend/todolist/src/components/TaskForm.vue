<template>
    <form @submit.prevent="submitTask">
        <input class="input-field" v-model="Description" placeholder="Task description" />
        <button class="button" type="submit">Add Task</button>
    </form>
</template>
  
<script>
export default {
    data() {
        return {
            Description: '',
            Completed: false
        };
    },
    methods: {
        submitTask() {
            const newTask = {
                description: this.Description,
                completed: this.Completed
            };
            this.$emit('new-task-created', newTask);
            this.Description = ''; // Reset for next entry
            this.Completed = false
        }
    }
};
</script>
  