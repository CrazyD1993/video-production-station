CREATE INDEX `topics_status_score_idx` ON `topics` (`status`,`score_total`);--> statement-breakpoint
CREATE INDEX `topics_updated_idx` ON `topics` (`updated_at`);