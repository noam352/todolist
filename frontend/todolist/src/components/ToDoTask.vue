<template>
    <div class="ToDoTask">
        <!-- Toggle between viewing and editing description -->
        <div class="task-description">
            <div v-if="!isEditing" @dblclick="startEditing">
                <p>{{ task.description }}</p>
            </div>
            <input v-else v-model="newDescription" @blur="emitUpdate" @keyup.enter="emitUpdate">
        </div>
        <div class="task-completed">
            <div :class="{ 'status-box': true, completed: task.completed, notCompleted: !task.completed }">
                {{ task.completed ? 'Completed' : 'Not Completed' }}
            </div>
        </div>
        <div class="task-actions">
            <button class="btn-complete" @click="emitComplete">Complete</button>
            <button class="btn-update" @click="emitUpdate">Update</button>
            <button class="btn-delete" @click="emitDelete">Delete</button>
        </div>
    </div>
</template>
  
<script>
export default {
    props: {
        task: Object
    },
    data() {
        return {
            isEditing: false,
            newDescription: ''
        };
    },
    methods: {
        emitComplete() {
            this.$emit('complete-task', this.task.id);
        },
        startEditing() {
            this.isEditing = true;
            this.newDescription = this.task.description; // Initialize with the current description
        },
        emitUpdate() {
            this.isEditing = false;
            if (this.newDescription === '') {
                this.newDescription = this.task.description;
            }
            this.$emit('update-task', this.task.id, this.newDescription);
        },
        emitDelete() {
            this.$emit('delete-task', this.task.id);
        }
    }
};
</script>


<style>
.ToDoTask {
    display: flex;
    align-items: center;
    /* justify-content: space-between; */
    padding: 10px;
    /* border-bottom: 1px solid #ddd; */
}

.task-description {
    flex-grow: 1;
    /* Allow the description to grow and take available space */
    margin-right: 20px;
    /* Add space between description and status */
    padding: 10px;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease;
}

.task-description:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.task-description p {
    margin: 0;
    font-size: 16px;
    line-height: 1.5;
    color: #333;
}

.task-description p::before {
    content: '\f0ca';
    /* FontAwesome icon code */
    font-family: 'FontAwesome';
    margin-right: 8px;
    color: #007bff;
}

.task-description input {
    width: 100%;
    padding: 8px;
    border: 2px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    box-sizing: border-box;
    /* Ensures padding doesn't increase the size */
    transition: border-color 0.3s ease;
}

.task-description input:focus {
    outline: none;
    border-color: #007bff;
    /* Highlight color when focused */
}

.status-box {
    padding: 5px 10px;
    text-align: center;
    border-radius: 10px;
    color: white;
    font-weight: bold;
    min-width: 120px;
    /* Set a minimum width for consistency */
}

.completed {
    background-color: #28a745;
    /* margin-right: 20px; */
    /* Green for completed tasks */
}

.notCompleted {
    background-color: #dc3545;
    /* margin-right: 20px; */
    /* Red for tasks not completed */
}

/* Base button styling */
.task-actions button {
    padding: 8px 15px;
    border: none;
    border-radius: 20px;
    /* Curved corners */
    font-weight: bold;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    /* Subtle shadow */
}

/* Hover effect for all buttons */
.task-actions button:hover {
    opacity: 0.8;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    /* More pronounced shadow on hover */
    transform: translateY(-2px);
    /* Slight lift */
}

/* Active state effect */
.task-actions button:active {
    transform: translateY(1px);
    box-shadow: 0 2px 3px rgba(0, 0, 0, 0.2);
}

/* Specific styles for each button type */
.btn-complete {
    background-color: #28a745;
    /* Green */
}

.btn-update {
    background-color: #ffc107;
    /* Yellow */
    color: black;
    /* For better readability */
}

.btn-delete {
    background-color: #dc3545;
    /* Red */
}
</style>