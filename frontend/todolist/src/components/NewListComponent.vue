<template>
    <div>
        <button class="button" v-if="!showForm" @click="showForm = true">Create New List</button>
        <div v-else>
            <input class="input-field" v-model="listName" placeholder="Enter list name">
            <button class="button" :disabled="!listName.trim()" @click="submitList">Submit</button>
        </div>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            showForm: false,
            listName: ''
        };
    },
    methods: {
        submitList() {
            if (this.listName.trim()) {
                this.$emit('list-created', this.listName);
                this.showForm = false;
                this.listName = '';
                // Do not reset the errorMessage here; let the parent handle it
            }
        }
    }
};
</script>
  
<style>
</style>
