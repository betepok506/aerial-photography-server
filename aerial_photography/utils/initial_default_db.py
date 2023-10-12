'''
Данный модуль содержит вспомогательные функции для инициализации
дефолтными значениями таблиц базы данных
'''
from aerial_photography import crud, schemas
from sqlalchemy.ext.asyncio import AsyncSession


async def initial_table_platform_name_sentinel(db: AsyncSession):
    '''
    Функция для инициализации таблицы `platform_name_sentinel` дефолтными значениями

    Parameters:
    -------------
    db: `AsyncSession`
        Асинхронный класс сессии подключения к SQLAlchemy
    '''
    added_values = ['Sentinel-1', 'Sentinel-2', 'Sentinel-3', 'Sentinel-5 Precursor']
    for value in added_values:
        search_result = await crud.platform_name_sentinel.search(db=db,
                                                                 obj_in=schemas.PlatformNameSentinelSearch(name=value))
        if len(search_result) == 0:
            await crud.platform_name_sentinel.create(db=db, obj_in=schemas.PlatformNameSentinelCreate(name=value))


async def initial_table_type_polygons_to_search_for(db: AsyncSession):
    '''
    Функция для инициализации таблицы `type_polygons_to_search_for` дефолтными значениями

    Parameters:
    -------------
    db: `AsyncSession`
        Асинхронный класс сессии подключения к SQLAlchemy
    '''
    added_values = ['Запросить 1 раз',
                    'Запросить n раз',
                    'Запрашивать с _ по _',
                    'Запрашивать всегда']
    for value in added_values:
        search_result = await crud.type_polygons_to_search_for.search(db=db,
                                                                      obj_in=schemas.TypePolygonsToSearchForSearch(
                                                                          name=value))
        if len(search_result) == 0:
            await crud.type_polygons_to_search_for.create(db=db, obj_in=schemas.TypePolygonsToSearchForSearch(
                name=value))

# async def initial_table_processing_level_sentinel(db: AsyncSession):
#     # TODO: Добавить значения для поиска в API Copernicus
#     '''
#     Функция для инициализации таблицы `platform_name_sentinel` дефолтными значениями
#
#     Parameters:
#     -------------
#     db: `AsyncSession`
#         Асинхронный класс сессии подключения к SQLAlchemy
#     '''
#     added_values = []
#     for value in added_values:
#         search_result = await crud.platform_name_sentinel.search(db=db,
#                                                                  obj_in=schemas.PlatformNameSentinelSearch(name=value))
#         if search_result is not None:
#             await crud.platform_name_sentinel.create(db=db, obj_in=schemas.PlatformNameSentinelCreate(name=value))
