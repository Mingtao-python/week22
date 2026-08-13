"""
Create a test corpus of 50+ documents for evaluation.
Generates documents across multiple subjects, grades, and permissions.
"""

import json
from pathlib import Path


def create_test_corpus():
    """Create 50+ test documents and manifest."""
    
    corpus_dir = Path(__file__).parent.parent / "data" / "test_corpus"
    corpus_dir.mkdir(parents=True, exist_ok=True)
    
    manifest = []
    doc_id = 1
    
    # Math documents (10 docs)
    math_topics = [
        "Algebra: Linear Equations and Systems",
        "Algebra: Quadratic Equations and Roots",
        "Algebra: Polynomials and Factoring",
        "Algebra: Exponents and Radicals",
        "Algebra: Rational Expressions",
        "Geometry: Triangles and Properties",
        "Geometry: Circles and Circumference",
        "Geometry: Volume and Surface Area",
        "Calculus: Limits and Continuity",
        "Calculus: Derivatives and Applications",
    ]
    
    for topic in math_topics:
        filename = f"math_{doc_id:03d}.txt"
        filepath = corpus_dir / filename
        
        content = f"""{topic}

{topic} is an essential concept in mathematics education.
Students at all grade levels encounter {topic} in their curriculum.

Key concepts:
- Understanding the fundamentals
- Applying to real-world problems
- Building problem-solving skills
- Connecting to other mathematical areas

This document provides comprehensive coverage of {topic}.
It includes examples, problems, and detailed explanations.
"""
        
        filepath.write_text(content)
        
        manifest.append({
            "document_id": f"math_{doc_id:03d}",
            "filename": filename,
            "type": "txt",
            "subject": "Mathematics",
            "grade": "9-12",
            "permission": "public",
            "expected_queries": [
                f"What is {topic.split(':')[0].lower()}?",
                f"Explain {topic}",
                f"How do you solve {topic.split(':')[0].lower()} problems?"
            ]
        })
        doc_id += 1
    
    # Physics documents (10 docs)
    physics_topics = [
        "Motion: Kinematics and Velocity",
        "Motion: Acceleration and Forces",
        "Energy: Potential and Kinetic",
        "Energy: Conservation of Energy",
        "Waves: Frequency and Wavelength",
        "Waves: Sound and Electromagnetic",
        "Heat: Temperature and Thermodynamics",
        "Electricity: Circuits and Current",
        "Magnetism: Magnetic Fields",
        "Light: Reflection and Refraction",
    ]
    
    for topic in physics_topics:
        filename = f"physics_{doc_id:03d}.txt"
        filepath = corpus_dir / filename
        
        content = f"""{topic}

{topic} is a fundamental topic in physics.
It explains the behavior of matter and energy.

Core principles:
- Mathematical formulations
- Real-world applications
- Experimental verification
- Historical development

Understanding {topic} is crucial for advanced physics.
This document explains the concepts thoroughly.
"""
        
        filepath.write_text(content)
        
        manifest.append({
            "document_id": f"physics_{doc_id:03d}",
            "filename": filename,
            "type": "txt",
            "subject": "Physics",
            "grade": "10-12",
            "permission": "public",
            "expected_queries": [
                f"Explain {topic}",
                f"What is {topic.split(':')[0].lower()}?",
            ]
        })
        doc_id += 1
    
    # Chemistry documents (10 docs)
    chemistry_topics = [
        "Atomic Structure: Electrons and Orbitals",
        "Bonding: Covalent and Ionic Bonds",
        "Reactions: Acids and Bases",
        "Reactions: Oxidation and Reduction",
        "Solutions: Concentration and pH",
        "Organic Chemistry: Hydrocarbons",
        "Organic Chemistry: Functional Groups",
        "Equilibrium: Reaction Rates",
        "Electrochemistry: Cells and Potentials",
        "Thermochemistry: Heat and Reactions",
    ]
    
    for topic in chemistry_topics:
        filename = f"chemistry_{doc_id:03d}.txt"
        filepath = corpus_dir / filename
        
        content = f"""{topic}

{topic} explores the fundamental nature of matter.
Chemical understanding begins with {topic.split(':')[0].lower()}.

Important concepts:
- Molecular structure
- Chemical behavior
- Energy considerations
- Quantitative relationships

Mastering {topic} is essential for chemistry success.
"""
        
        filepath.write_text(content)
        
        manifest.append({
            "document_id": f"chemistry_{doc_id:03d}",
            "filename": filename,
            "type": "txt",
            "subject": "Chemistry",
            "grade": "10-12",
            "permission": "public",
            "expected_queries": [
                f"What is {topic}?",
                f"Explain {topic.lower()}",
            ]
        })
        doc_id += 1
    
    # Biology documents (10 docs)
    biology_topics = [
        "Cell Biology: Cell Structure and Function",
        "Cell Biology: Photosynthesis and Respiration",
        "Genetics: DNA and Inheritance",
        "Genetics: Mutations and Evolution",
        "Ecology: Organisms and Populations",
        "Ecology: Ecosystems and Food Webs",
        "Human Body: Skeletal and Muscular Systems",
        "Human Body: Circulatory and Respiratory",
        "Immunology: Immune System Defense",
        "Microbiology: Bacteria and Viruses",
    ]
    
    for topic in biology_topics:
        filename = f"biology_{doc_id:03d}.txt"
        filepath = corpus_dir / filename
        
        content = f"""{topic}

{topic} examines the living world at multiple scales.
From cells to organisms, {topic} provides crucial insights.

Key areas:
- Microscopic structures
- Biochemical processes
- Organism behavior
- Population dynamics

{topic} is fundamental to biological science.
"""
        
        filepath.write_text(content)
        
        manifest.append({
            "document_id": f"biology_{doc_id:03d}",
            "filename": filename,
            "type": "txt",
            "subject": "Biology",
            "grade": "9-12",
            "permission": "public",
            "expected_queries": [
                f"What is {topic.split(':')[0].lower()}?",
                f"Explain {topic}",
            ]
        })
        doc_id += 1
    
    # History/Literature documents (10 docs)
    history_topics = [
        "Renaissance: Art and Culture",
        "Renaissance: Scientific Revolution",
        "Enlightenment: Philosophy and Ideas",
        "Industrial Revolution: Technology",
        "Revolutions: American and French",
        "Imperialism: Colonization and Effects",
        "World Wars: Causes and Consequences",
        "Cold War: Tensions and Conflicts",
        "Modern Era: Globalization",
        "Contemporary: 21st Century Challenges",
    ]
    
    for topic in history_topics:
        filename = f"history_{doc_id:03d}.txt"
        filepath = corpus_dir / filename
        
        content = f"""{topic}

{topic} shaped the modern world.
Understanding {topic} helps us comprehend current events.

Historical significance:
- Key events and figures
- Social transformations
- Cultural developments
- Economic changes

{topic} provides essential historical context.
"""
        
        filepath.write_text(content)
        
        manifest.append({
            "document_id": f"history_{doc_id:03d}",
            "filename": filename,
            "type": "txt",
            "subject": "History",
            "grade": "8-12",
            "permission": "public",
            "expected_queries": [
                f"What was the {topic.split(':')[0].lower()}?",
                f"Explain {topic}",
            ]
        })
        doc_id += 1
    
    # Save manifest
    manifest_file = corpus_dir / "manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    
    print(f"✅ Created {len(manifest)} test documents")
    print(f"📁 Location: {corpus_dir}")
    print(f"📋 Manifest: {manifest_file}")
    
    return corpus_dir, manifest


if __name__ == "__main__":
    create_test_corpus()
