<script lang="ts">
    import { onMount } from "svelte";
    import JobEntry from "$lib/components/JobEntry.svelte";
    import AnalysisSection from "$lib/components/AnalysisSection.svelte";
    import AnalysisPoint from "$lib/components/AnalysisPoint.svelte";
    import AnalysisInsight from "$lib/components/AnalysisInsight.svelte";
    import AnalysisScore from "$lib/components/AnalysisScore.svelte";

    let jobs: any[] = [];
    let selectedJob: any = null;

    onMount(async () => {
        const response = await fetch("http://localhost:8000/api/jobs");
        const data = await response.json();
        jobs = data.jobs;
    });

    async function selectJob(job: any) {
        const response = await fetch("http://localhost:8000/api/job/" + job.id);
        const data = await response.json();
        selectedJob = data;
    }

    async function generateAnalysis(job: any) {
        const response = await fetch(
            "http://localhost:8000/api/analysis/" + job.id,
        );
        const data = await response.json();
        console.log(data);
        return data;
    }
</script>

<div class="flex h-screen">
    <!-- Column 1 -->
    <aside class="w-80 bg-white border-r border-border flex flex-col">
        <div class="p-4 font-bold border-b border-border">
            <div class="font-semibold">Jobs</div>
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
    <main class="bg-white border-r border-border flex flex-col flex-1">
        <div class="overflow-y-auto p-8">
            {#if selectedJob}
                <div id="job-details" class="mx-auto max-w-3xl">
                    <div class="border-border mb-8 border-b pb-6">
                        <div
                            class="mb-4 flex items-start justify-between gap-4"
                        >
                            <h1
                                class="job-title text-foreground flex-1 text-2xl font-bold"
                            >
                                {selectedJob.title}
                            </h1>
                            <!-- <button class="border-border hover:bg-accent flex items-center gap-2 rounded-md border px-3 py-1.5 text-sm">Edit</button> -->
                        </div>
                        <div
                            class="text-muted-foreground mb-4 flex flex-wrap items-center gap-3 text-sm"
                        >
                            <span class="job-company"
                                >{selectedJob.company}</span
                            ><span>•</span>
                            <div class="job-location flex items-center gap-1.5">
                                <span>{selectedJob.location}</span>
                            </div>
                            <span
                                class="job-source border-border rounded-md border px-2 py-0.5 text-xs"
                                >{selectedJob.source}</span
                            >
                        </div>
                        <a
                            target="_blank"
                            rel="noopener noreferrer"
                            href={selectedJob.url}
                            class="job-url-button text-white bg-[#050708] hover:bg-[#050708]/90 focus:ring-4 focus:outline-none focus:ring-[#050708]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#050708]/50 dark:hover:bg-[#050708]/30 me-2 mb-2"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                class="w-4 h-4 me-2 -ms-1 lucide lucide-external-link-icon lucide-external-link"
                            >
                                <path d="M15 3h6v6" />
                                <path d="M10 14 21 3" />
                                <path
                                    d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"
                                />
                            </svg>
                            <span class="font-semibold">View Source</span>
                        </a>
                    </div>
                    <div class="job-description prose max-w-none">
                        <p>{@html selectedJob.description}</p>
                    </div>
                </div>
            {:else}
                <div
                    id="job-details-placeholder"
                    class="flex h-full flex-col items-center justify-center space-y-4"
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
    <aside class="w-96 bg-white flex flex-col">
        <div
            class="p-4 font-bold border-b border-border flex flex-shrink-0 items-center gap-2"
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
                        class="cursor-pointer group relative inline-flex items-center justify-center rounded-lg border border-slate-900/10 bg-white/40 px-8 py-3 font-medium text-slate-800 backdrop-blur-md transition-all duration-300 hover:bg-white/60"
                        onclick={async () => {
                            const analysis =
                                await generateAnalysis(selectedJob);
                            selectedJob = { ...selectedJob, analysis };
                        }}
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

                        <span>Generate Analysis</span>
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
