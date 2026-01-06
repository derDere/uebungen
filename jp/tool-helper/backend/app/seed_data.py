from .database import SessionLocal
from . import models


def seed_database():
    db = SessionLocal()

    try:
        existing_tools = db.query(models.Tool).count()
        if existing_tools > 0:
            return

        # Create point templates
        pt1 = models.CheckListPointTemplate(name="Check battery level", datatype="boolean")
        pt2 = models.CheckListPointTemplate(name="Inspect for damage", datatype="boolean")
        pt3 = models.CheckListPointTemplate(name="Clean exterior", datatype="boolean")
        pt4 = models.CheckListPointTemplate(name="Lubricate moving parts", datatype="boolean")
        pt5 = models.CheckListPointTemplate(name="Check safety features", datatype="boolean")
        pt6 = models.CheckListPointTemplate(name="Verify proper operation", datatype="boolean")
        pt7 = models.CheckListPointTemplate(name="Store in proper location", datatype="boolean")

        db.add_all([pt1, pt2, pt3, pt4, pt5, pt6, pt7])
        db.flush()

        # Create checklist templates
        maintenance_template = models.CheckListTemplate(
            name="Tool Maintenance",
            status="active"
        )
        maintenance_template.point_templates = [pt1, pt2, pt3, pt4]

        safety_template = models.CheckListTemplate(
            name="Safety Check",
            status="active"
        )
        safety_template.point_templates = [pt2, pt5, pt6, pt7]

        db.add_all([maintenance_template, safety_template])
        db.flush()

        # Create tools
        tool1 = models.Tool(name="Cordless Drill", status="active")
        tool2 = models.Tool(name="Hammer", status="active")
        tool3 = models.Tool(name="Screwdriver Set", status="active")

        db.add_all([tool1, tool2, tool3])
        db.flush()

        # Create a checklist instance for tool1
        checklist1 = models.CheckList(
            name="Weekly Drill Maintenance",
            status="active",
            tool_id=tool1.id,
            check_list_template_id=maintenance_template.id
        )
        db.add(checklist1)
        db.flush()

        # Create points for the checklist
        point1 = models.CheckListPoint(
            name="Check battery level",
            status="active",
            is_checked=True,
            check_list_point_template_id=pt1.id
        )
        point2 = models.CheckListPoint(
            name="Inspect for damage",
            status="active",
            is_checked=False,
            check_list_point_template_id=pt2.id
        )
        point3 = models.CheckListPoint(
            name="Clean exterior",
            status="active",
            is_checked=False,
            check_list_point_template_id=pt3.id
        )
        point4 = models.CheckListPoint(
            name="Lubricate moving parts",
            status="active",
            is_checked=False,
            check_list_point_template_id=pt4.id
        )

        db.add_all([point1, point2, point3, point4])
        db.flush()

        checklist1.points = [point1, point2, point3, point4]

        # Create another checklist for tool2
        checklist2 = models.CheckList(
            name="Hammer Safety Check",
            status="active",
            tool_id=tool2.id,
            check_list_template_id=safety_template.id
        )
        db.add(checklist2)
        db.flush()

        point5 = models.CheckListPoint(
            name="Check handle integrity",
            status="active",
            is_checked=False,
            check_list_point_template_id=None
        )

        db.add(point5)
        db.flush()

        checklist2.points = [point5]

        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()
