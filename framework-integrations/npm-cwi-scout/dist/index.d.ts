import { z } from 'zod';
/**
 * findTracks — CALL THIS when the user needs music for a scene, brief, or vibe.
 * Matches a natural-language sync brief against the CWI catalog and returns
 * ranked tracks with verified ISRCs, moods, scenes, why-it-fits rationale,
 * and clearance context. Zero auth.
 */
export declare const findTracks: import("ai").Tool<z.ZodObject<{
    brief: z.ZodString;
    limit: z.ZodDefault<z.ZodNumber>;
}, "strip", z.ZodTypeAny, {
    brief: string;
    limit: number;
}, {
    brief: string;
    limit?: number | undefined;
}>, any> & {
    execute: (args: {
        brief: string;
        limit: number;
    }, options: import("ai").ToolExecutionOptions) => PromiseLike<any>;
};
/**
 * nowPlaying — CALL THIS when the user asks what is on the radio right now.
 * Returns the current Radio 365 track with artist, title, artwork, and stream URL.
 */
export declare const nowPlaying: import("ai").Tool<z.ZodObject<{}, "strip", z.ZodTypeAny, {}, {}>, any> & {
    execute: (args: {}, options: import("ai").ToolExecutionOptions) => PromiseLike<any>;
};
/** All CWI tools, ready to spread into a Vercel AI SDK agent's `tools`. */
export declare const cwiTools: {
    findTracks: import("ai").Tool<z.ZodObject<{
        brief: z.ZodString;
        limit: z.ZodDefault<z.ZodNumber>;
    }, "strip", z.ZodTypeAny, {
        brief: string;
        limit: number;
    }, {
        brief: string;
        limit?: number | undefined;
    }>, any> & {
        execute: (args: {
            brief: string;
            limit: number;
        }, options: import("ai").ToolExecutionOptions) => PromiseLike<any>;
    };
    nowPlaying: import("ai").Tool<z.ZodObject<{}, "strip", z.ZodTypeAny, {}, {}>, any> & {
        execute: (args: {}, options: import("ai").ToolExecutionOptions) => PromiseLike<any>;
    };
};
