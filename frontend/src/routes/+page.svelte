<script lang="ts">
    import { onMount } from "svelte";
    import JobEntry from "$lib/components/JobEntry.svelte";
    import AnalysisSection from "$lib/components/AnalysisSection.svelte";
    import AnalysisPoint from "$lib/components/AnalysisPoint.svelte";
    import AnalysisInsight from "$lib/components/AnalysisInsight.svelte";
    import AnalysisScore from "$lib/components/AnalysisScore.svelte";
    import JobDetails from "$lib/components/JobDetails.svelte";

    let jobs: any[] = $state([]);
    let selectedJob: any = $state(null);

    let isGenerating = $state(false);

    onMount(async () => {
        try {
            const response = await fetch("http://localhost:8000/api/jobs");
            
            if (response.status === 200) {
                const data = await response.json();
                jobs = data.jobs;
            }
            else {
                console.log(response.status);
            }
        }
        catch (error) {
            console.error(error);
        }
    });

    async function selectJob(job: any) {
        try {
            const response = await fetch("http://localhost:8000/api/jobs/" + job.id);

            if (response.status === 200) {
                const data = await response.json();
                selectedJob = data;
            }
            else {
                console.log(response.status);
            }
        }
        catch (error) {
            console.error(error);
        }
    }

    async function generateAnalysis(job: any) {
        isGenerating = true;

        try {
            const response = await fetch("http://localhost:8000/api/analysis/" + job.id);
            
            if (response.status === 200) {
                const data = await response.json();
                return data;
            }
            else {
                console.log(response.status);
            }
        }
        catch (error) {
            console.error(error);
        }
        finally {
            isGenerating = false;
        }
    }

    async function updateJobs() {
        try {
            const response = await fetch("http://localhost:8000/api/jobs/update", {
                method: "POST"
            });
            
            if (response.status !== 200) {
                console.log(response.status);
            }
        }
        catch (error) {
            console.error(error);
        }
    }
</script>

<div class="flex flex-grow overflow-y-auto">
    <!-- Column 1 -->
    <aside
        class="w-80 bg-white border-r border-border flex flex-col dark:text-white dark:bg-gray-900 dark:border-gray-600"
    >
        <div class="p-4 font-bold border-b border-border dark:border-gray-600">
            <div class="flex justify-between items-center">
                <div class="font-semibold">Jobs</div>
                <div class="flex space-x-1">
                    <a
                        href="/create"
                        class="p-1 border-border border-1 rounded-lg cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-800"
                        aria-label="Add Job"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            class="lucide lucide-plus-icon lucide-plus h-4 w-4"
                            ><path d="M5 12h14" /><path d="M12 5v14" /></svg
                        >
                    </a>
                    <a
                        onclick={async () => updateJobs()}
                        href="/#"
                        class="p-1 border-border border-1 rounded-lg cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-800"
                        aria-label="Refresh Jobs"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            class="lucide lucide-refresh-cw-icon lucide-refresh-cw h-4 w-4"
                            ><path
                                d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"
                            /><path d="M21 3v5h-5" /><path
                                d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"
                            /><path d="M8 16H3v5" /></svg
                        >
                    </a>
                </div>
            </div>
        </div>
        <div class="overflow-y-auto p-3">
            {#each jobs as job (job.id)}
                <JobEntry
                    {job}
                    {selectedJob}
                    onclickFunc={() => selectJob(job)}
                />
            {/each}
        </div>
    </aside>

    <!-- Column 2 -->
    <main
        class="bg-white border-r border-border flex flex-col flex-1 dark:bg-gray-900 dark:text-white dark:border-gray-600"
    >
        <div class="overflow-y-auto p-8">
            {#if selectedJob}
                <JobDetails {...selectedJob} />
            {:else}
                <div
                    id="job-details-placeholder"
                    class="flex h-full flex-col items-center justify-center space-y-4 p-16"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="48"
                        height="48"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="lucide lucide-square-dashed-icon lucide-square-dashed"
                        ><path d="M5 3a2 2 0 0 0-2 2" /><path
                            d="M19 3a2 2 0 0 1 2 2"
                        /><path d="M21 19a2 2 0 0 1-2 2" /><path
                            d="M5 21a2 2 0 0 1-2-2"
                        /><path d="M9 3h1" /><path d="M9 21h1" /><path
                            d="M14 3h1"
                        /><path d="M14 21h1" /><path d="M3 9v1" /><path
                            d="M21 9v1"
                        /><path d="M3 14v1" /><path d="M21 14v1" /></svg
                    >
                    <p class="text-muted-foreground">
                        Select a job to view details
                    </p>
                </div>
            {/if}
        </div>
    </main>

    <!-- Column 3 -->
    <aside class="w-96 bg-white flex flex-col dark:bg-gray-900 dark:text-white">
        <div
            class="p-4 font-bold border-b border-border flex flex-shrink-0 items-center gap-2 dark:border-gray-600"
        >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="lucide lucide-sparkle-icon lucide-sparkle h-5 w-5"
            >
                <path
                    d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z"
                />
            </svg>
            <div class="text-foreground font-semibold">AI Analysis</div>
        </div>
        <div class="overflow-y-auto p-4 space-y-3">
            {#if selectedJob == null}
                <p>Select a job to view AI analysis</p>
            {:else if selectedJob.analysis == null}
                <div class="flex h-48 w-full items-center justify-center">
                    <button
                        class="cursor-pointer group relative inline-flex items-center justify-center rounded-lg border border-slate-900/10 bg-white/40 px-8 py-3 font-medium text-slate-800 backdrop-blur-md transition-all duration-300 hover:bg-gradient-to-r from-blue-600 to-purple-600 hover:text-white dark:text-white dark:bg-gray-800 disabled:cursor-not-allowed disabled:bg-gradient-to-r disabled:text-white animate-gradient"
                        onclick={async () => {
                            const analysis =
                                await generateAnalysis(selectedJob);
                            selectedJob = { ...selectedJob, analysis };
                        }}
                        disabled={isGenerating}
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="2"
                            stroke="currentColor"
                            class="mr-3 h-6 w-6"
                        >
                            <path
                                d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72"
                            /><path d="m14 7 3 3" /><path d="M5 6v4" /><path
                                d="M19 14v4"
                            /><path d="M10 2v2" /><path d="M7 8H3" /><path
                                d="M21 16h-4"
                            /><path d="M11 3H9" />
                        </svg>

                        <span>
                            {#if !isGenerating}
                                Generate Analysis
                            {:else}
                                Generating Analysis...
                            {/if}
                        </span>
                    </button>
                </div>
            {:else}
                <AnalysisScore
                    score={selectedJob.analysis.candidate_fit_score}
                    summary={selectedJob.analysis.application_summary}
                />

                <AnalysisSection title="Top Strengths">
                    {#each selectedJob.analysis.top_strengths as strength}
                        <AnalysisPoint color="green" point={strength} />
                    {/each}
                </AnalysisSection>

                <AnalysisSection title="Key Gaps">
                    {#each selectedJob.analysis.key_gaps as gap}
                        <AnalysisPoint color="red" point={gap} />
                    {/each}
                </AnalysisSection>

                <AnalysisSection title="Possible Interview Questions">
                    {#each selectedJob.analysis.possible_questions as question}
                        <AnalysisPoint color="yellow" point={question} />
                    {/each}
                </AnalysisSection>

                <AnalysisSection title="Insights">
                    {#each selectedJob.analysis.insights_list as insight}
                        <AnalysisInsight {...insight} />
                    {/each}
                </AnalysisSection>
            {/if}
        </div>
    </aside>
</div>

<style>
    .animate-gradient {
        background-size: 300%;
        animation: animatedgradient 6s ease infinite alternate;
    }

    @keyframes animatedgradient {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
</style>
