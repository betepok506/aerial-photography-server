import pytest
from sqlalchemy.orm import Session
from aerial_photography import crud
from aerial_photography.tests.utils.utils import random_lower_string
from aerial_photography.schemas.space_programs import SpaceProgramsCreate, SpaceProgramsUpdate


def test_create_space_program(db: Session) -> None:
    space_program = random_lower_string()
    space_program_in = SpaceProgramsCreate(name=space_program)

    program = crud.space_programs.create(db=db, obj_in=space_program_in)
    assert program.name == space_program


def test_get_space_program(db: Session) -> None:
    space_program = random_lower_string()
    space_program_in = SpaceProgramsCreate(name=space_program)

    program = crud.space_programs.create(db=db, obj_in=space_program_in)
    stored_program = crud.space_programs.get(db=db, id=program.id)
    assert stored_program
    assert program.id == stored_program.id
    assert program.name == stored_program.name


def test_update_space_program(db: Session) -> None:
    space_program = random_lower_string()
    space_program_in = SpaceProgramsCreate(name=space_program)
    program = crud.space_programs.create(db=db, obj_in=space_program_in)

    new_program = random_lower_string()
    item_update = SpaceProgramsUpdate(id=program.id, name=new_program)
    updated_program = crud.space_programs.update(db=db, db_obj=program, obj_in=item_update)
    assert program.id == updated_program.id
    assert updated_program.name == new_program


def test_delete_space_program(db: Session) -> None:
    space_program = random_lower_string()
    space_program_in = SpaceProgramsCreate(name=space_program)
    program = crud.space_programs.create(db=db, obj_in=space_program_in)

    removed_program = crud.space_programs.remove(db=db, id=program.id)
    stored_program = crud.space_programs.get(db=db, id=program.id)
    assert stored_program is None
    assert removed_program.id == program.id
    assert removed_program.name == program.name
