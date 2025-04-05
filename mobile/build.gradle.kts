import com.diffplug.gradle.spotless.SpotlessExtension
import com.diffplug.gradle.spotless.SpotlessPlugin
import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
    alias(libs.plugins.spotless) apply false
    alias(libs.plugins.android.library) apply false
    alias(libs.plugins.jetbrains.kotlin.jvm) apply false
}

subprojects {
    apply<SpotlessPlugin>()
    configure<SpotlessExtension> {
        kotlin {
            target("src/**/*.kt")
            targetExclude("build/**/*.kt")
        }

        kotlinGradle {
            target("*.kts")
            ktlint()
                .editorConfigOverride(
                    mapOf(
                        "max_line_length" to "140",
                        "ij_kotlin_allow_trailing_comma" to "false",
                        "ktlint_standard_filename" to "disabled",
                        "ij_kotlin_allow_trailing_comma_on_call_site" to "false",
                        "ij_kotlin_line_break_after_multiline_when_entry" to "false",
                        "ktlint_standard_no-empty-first-line-in-method-block" to "enabled",
                        "ktlint_function_signature_body_expression_wrapping" to "multiline",
                        "ktlint_function_signature_rule_force_multiline_when_parameter_count_greater_or_equal_than" to "2",
                        "ktlint_function_naming_ignore_when_annotated_with" to "Composable, Test"
                    )
                )
        }
    }

    afterEvaluate {
        tasks.withType<KotlinCompile> {
            finalizedBy("spotlessApply")
        }
    }
}