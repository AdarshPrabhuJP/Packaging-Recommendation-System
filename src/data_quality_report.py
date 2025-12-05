"""
Data Quality Report Generator
Creates a comprehensive markdown report of data quality analysis.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.data_validation import generate_validation_report
from src.data_cleaning import get_feature_statistics, encode_categorical_variables
from src.database_utils import get_database_statistics


def generate_quality_report():
    """Generate comprehensive data quality report in Markdown format"""
    
    # Get all reports
    validation_report = generate_validation_report()
    db_stats = get_database_statistics()
    feature_stats = get_feature_statistics()
    encodings = encode_categorical_variables()
    
    # Generate markdown report
    report_lines = []
    
    # Header
    report_lines.append("# Data Quality Report")
    report_lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"\n**Project:** Packaging Recommendation System")
    report_lines.append("\n---\n")
    
    # Dataset Overview
    report_lines.append("## 📊 Dataset Overview\n")
    report_lines.append(f"- **Total Materials:** {db_stats['total_materials']}")
    report_lines.append(f"- **Recyclable Materials:** {db_stats['recyclable_materials']} ({db_stats['recyclable_percentage']:.1f}%)")
    report_lines.append(f"- **Non-Recyclable Materials:** {db_stats['total_materials'] - db_stats['recyclable_materials']}")
    report_lines.append(f"- **Number of Features:** 11 (10 attributes + 1 ID)")
    report_lines.append("\n---\n")
    
    # Missing Values
    report_lines.append("## 🔍 Missing Value Analysis\n")
    missing = validation_report['missing_values']
    total_missing = sum(missing['missing_values'].values())
    
    if total_missing == 0:
        report_lines.append("✅ **No missing values found** - Dataset is 100% complete!\n")
    else:
        report_lines.append(f"⚠️ **Found {total_missing} missing values:**\n")
        report_lines.append("| Column | Missing Count | Completeness |")
        report_lines.append("|--------|---------------|--------------|")
        for col, count in missing['missing_values'].items():
            if count > 0:
                completeness = missing['completeness_percentage'][col]
                report_lines.append(f"| {col} | {count} | {completeness:.1f}% |")
    
    report_lines.append("\n---\n")
    
    # Statistical Summary
    report_lines.append("## 📈 Statistical Summary\n")
    report_lines.append("### Numerical Features\n")
    report_lines.append("| Feature | Min | Max | Mean | Std Dev |")
    report_lines.append("|---------|-----|-----|------|---------|")
    
    for feature, stats in feature_stats.items():
        report_lines.append(
            f"| {feature} | {stats['min']:.2f} | {stats['max']:.2f} | "
            f"{stats['mean']:.2f} | {stats['std']:.2f} |"
        )
    
    report_lines.append("\n### Database Averages\n")
    report_lines.append(f"- **Average Cost:** ${db_stats['avg_cost']:.2f}")
    report_lines.append(f"- **Average CO₂ Footprint:** {db_stats['avg_co2']:.2f}")
    report_lines.append(f"- **Average Biodegradability:** {db_stats['avg_biodegradability']:.1f}/10")
    report_lines.append(f"- **Average Durability:** {db_stats['avg_durability']:.1f}/10")
    
    report_lines.append("\n---\n")
    
    # Outlier Detection
    report_lines.append("## 🎯 Outlier Detection\n")
    outliers = validation_report['outliers']
    total_outliers = sum(o['count'] for o in outliers.values())
    
    if total_outliers == 0:
        report_lines.append("✅ **No outliers detected** - All values are within normal ranges.\n")
    else:
        report_lines.append(f"⚠️ **Found {total_outliers} outliers:**\n")
        report_lines.append("| Feature | Outlier Count | Valid Range |")
        report_lines.append("|---------|---------------|-------------|")
        for field, data in outliers.items():
            if data['count'] > 0:
                range_str = f"[{data['lower_bound']:.2f}, {data['upper_bound']:.2f}]"
                report_lines.append(f"| {field} | {data['count']} | {range_str} |")
    
    report_lines.append("\n---\n")
    
    # Range Validation
    report_lines.append("## ✅ Range Validation\n")
    range_val = validation_report['range_validation']
    
    if range_val['valid']:
        report_lines.append("✅ **All values within expected ranges**\n")
        report_lines.append("- Durability scores: 0-10 ✓")
        report_lines.append("- Biodegradability scores: 0-10 ✓")
        report_lines.append("- Cost values: Non-negative ✓")
        report_lines.append("- CO₂ values: Non-negative ✓")
    else:
        report_lines.append(f"⚠️ **Found {len(range_val['violations'])} violations:**\n")
        for violation in range_val['violations']:
            report_lines.append(f"- **{violation['field']}:** {violation['issue']} ({violation['count']} records)")
    
    report_lines.append("\n---\n")
    
    # Categorical Variables
    report_lines.append("## 🏷️ Categorical Variables\n")
    report_lines.append(f"### Material Types ({len(encodings['material_type'])} unique)\n")
    for mat_type, code in sorted(encodings['material_type'].items(), key=lambda x: x[1]):
        report_lines.append(f"- {mat_type} (code: {code})")
    
    report_lines.append(f"\n### Recommended Uses ({len(encodings['recommended_use'])} unique)\n")
    for use, code in sorted(encodings['recommended_use'].items(), key=lambda x: x[1]):
        report_lines.append(f"- {use} (code: {code})")
    
    report_lines.append("\n---\n")
    
    # Overall Assessment
    report_lines.append("## 🎯 Overall Data Quality Assessment\n")
    status = validation_report['overall_status']
    
    if status == 'PASS':
        report_lines.append("### ✅ **EXCELLENT**\n")
        report_lines.append("The dataset is of high quality with:")
        report_lines.append("- ✅ No missing values")
        report_lines.append("- ✅ All values within valid ranges")
        report_lines.append("- ✅ Proper data types")
        report_lines.append("- ✅ Consistent formatting")
        report_lines.append("\n**Recommendation:** Dataset is ready for analysis and modeling.")
    else:
        report_lines.append("### ⚠️ **ISSUES FOUND**\n")
        report_lines.append("Please review the issues identified above.")
        report_lines.append("\n**Recommendation:** Address data quality issues before proceeding.")
    
    report_lines.append("\n---\n")
    report_lines.append(f"\n*Report generated by Data Quality Report Generator v1.0*")
    
    return "\n".join(report_lines)


if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING DATA QUALITY REPORT")
    print("=" * 60)
    
    print("\n📊 Analyzing data quality...")
    report = generate_quality_report()
    
    # Save report
    output_file = Path(__file__).parent.parent / 'DATA_QUALITY_REPORT.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report generated successfully!")
    print(f"📄 Saved to: {output_file}")
    
    # Also print to console
    print("\n" + "=" * 60)
    print("REPORT PREVIEW:")
    print("=" * 60)
    print(report)
