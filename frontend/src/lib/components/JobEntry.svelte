<script lang="ts">
    let { job, selectedJob, onclickFunc } = $props();
</script>


<button
    class="job-entry-button mb-1 cursor-pointer hover:bg-accent w-full rounded-lg p-4 text-left {selectedJob?.id === job.id ? 'bg-blue-500 text-white hover:bg-blue-600' : ''}"
    onclick={onclickFunc}
>
    <div class="mb-3">
        <h3 class="text-base leading-tight font-bold">
            {job.title}
        </h3>
        <p class="text-muted-foreground mt-1 text-sm">
            {job.company}
        </p>
    </div>

    <div class="flex items-center justify-between gap-4">
        <div class="flex-grow">
            <div class="text-muted-foreground text-xs">
                <span>{job.location}</span>
            </div>
        </div>
        <div class="flex-shrink-0">
            <span
                class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-blue-700/10 ring-inset"
                >{job.source}</span
            >
        </div>
    </div>
</button>
